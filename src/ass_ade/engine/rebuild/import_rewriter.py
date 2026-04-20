"""Import Rewriter — predictive AST-aware import path correction after materialize.

Problem: the rebuild engine moves source files from their original locations into
tier directories (a0_qk_constants/, a1_at_functions/, etc.). Any cross-file import
that used a bare module name (e.g. `from utils import X`) becomes broken because
`utils.py` is now at `a1_at_functions/utils.py`.

This module:
  1. Builds an old-stem → new-qualified-name mapping from the written_modules dict
     produced by materialize_plan (e.g. "utils" → "a1_at_functions.utils").
  2. Walks every .py file in the rebuilt output directory.
  3. Rewrites `from MODULE import X` and `from .MODULE import X` lines where MODULE
     matches a moved stem to use the correct fully-qualified tier path.
  4. Validates each rewritten file parses cleanly; preserves the original on failure.

Scope: only fixes `from X import Y` patterns. Bare `import X` statements are left
untouched — they are less common in tier-structured code and the aliasing required
to fix them safely is non-trivial.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

_TIER_DIRS = frozenset({
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
    "tools",
})

# Regex patterns for the two import forms we rewrite
_FROM_ABS = re.compile(r"^(\s*from\s+)([\w][\w.]*)(\s+import\s+.+)$")
_FROM_REL = re.compile(r"^(\s*from\s+\.)([\w][\w.]*)(\s+import\s+.+)$")


def _extract_tier(dest_path: Path) -> str | None:
    """Return the tier directory name from a written dest path, or None."""
    for part in dest_path.parts:
        if part in _TIER_DIRS:
            return part
    return None


def build_stem_map(written_modules: dict[str, str]) -> dict[str, str]:
    """Build {bare_stem → qualified_name} from materialize_plan's written_modules.

    Example:
        written_modules = {
            "/old/proj/utils.py":  "/out/20260420/a1_at_functions/utils.py",
            "/old/proj/config.py": "/out/20260420/a0_qk_constants/config.py",
        }
        →  {"utils": "a1_at_functions.utils", "config": "a0_qk_constants.config"}
    """
    stem_map: dict[str, str] = {}
    for _src, dest in written_modules.items():
        dest_path = Path(dest)
        tier = _extract_tier(dest_path)
        if tier:
            stem = dest_path.stem
            # Don't map __init__ or test files
            if stem.startswith("__") or stem.startswith("test_"):
                continue
            qualified = f"{tier}.{stem}"
            # First occurrence wins (oldest source path, as materialize sorts by mtime desc)
            stem_map.setdefault(stem, qualified)
    return stem_map


def _rewrite_line(line: str, stem_map: dict[str, str]) -> tuple[str, bool]:
    """Rewrite a single import line if it references a moved module.

    Returns (new_line, changed).  Always preserves the original line ending.
    """
    trail = "\n" if line.endswith("\n") else ""

    # from MODULE import X  (absolute)
    m = _FROM_ABS.match(line)
    if m:
        prefix, mod_name, suffix = m.groups()
        # Only rewrite bare stems (no dots), not already-qualified imports
        if "." not in mod_name and mod_name in stem_map:
            new_line = f"{prefix}{stem_map[mod_name]}{suffix}{trail}"
            return new_line, new_line != line

    # from .MODULE import X  (relative -> absolute)
    m = _FROM_REL.match(line)
    if m:
        prefix, mod_name, suffix = m.groups()
        if mod_name in stem_map:
            indent = prefix[: len(prefix) - len(prefix.lstrip())]
            new_line = f"{indent}from {stem_map[mod_name]}{suffix}{trail}"
            return new_line, new_line != line

    return line, False


def rewrite_imports(
    target_root: Path,
    written_modules: dict[str, str],
) -> dict[str, Any]:
    """Walk target_root and rewrite broken imports for all moved modules.

    Args:
        target_root:     The materialized rebuild directory.
        written_modules: {old_src_path → new_dest_path} from materialize_plan receipt.

    Returns:
        {
            "stem_map":        {"utils": "a1_at_functions.utils", ...},
            "files_checked":   N,
            "files_rewritten": N,
            "total_changes":   N,
            "rewritten":       [{"file": "a1_at_functions/app.py", "changes": 2}, ...],
            "skipped_syntax":  [{"file": "...", "reason": "..."}],
        }
    """
    stem_map = build_stem_map(written_modules)
    if not stem_map:
        return {
            "stem_map": {},
            "files_checked": 0,
            "files_rewritten": 0,
            "total_changes": 0,
            "rewritten": [],
            "skipped_syntax": [],
        }

    files_checked = 0
    files_rewritten = 0
    total_changes = 0
    rewritten: list[dict[str, Any]] = []
    skipped_syntax: list[dict[str, Any]] = []

    for py_file in sorted(target_root.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        try:
            source = py_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        files_checked += 1
        new_lines = []
        file_changes = 0

        for line in source.splitlines(keepends=True):
            new_line, changed = _rewrite_line(line, stem_map)
            new_lines.append(new_line)
            if changed:
                file_changes += 1

        if file_changes == 0:
            continue

        new_source = "".join(new_lines)

        # Validate the rewritten source parses before writing
        try:
            ast.parse(new_source)
        except SyntaxError as exc:
            skipped_syntax.append({
                "file":   py_file.relative_to(target_root).as_posix(),
                "reason": f"rewrite produced syntax error: {exc}",
            })
            continue  # preserve original

        py_file.write_text(new_source, encoding="utf-8")
        files_rewritten += 1
        total_changes += file_changes
        rewritten.append({
            "file":    py_file.relative_to(target_root).as_posix(),
            "changes": file_changes,
        })

    return {
        "stem_map":        stem_map,
        "files_checked":   files_checked,
        "files_rewritten": files_rewritten,
        "total_changes":   total_changes,
        "rewritten":       rewritten,
        "skipped_syntax":  skipped_syntax,
    }
