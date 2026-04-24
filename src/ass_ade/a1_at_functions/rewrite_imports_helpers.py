"""Tier a1 — assimilated function 'rewrite_imports'

Assimilated from: rebuild/import_rewriter.py:108-193
"""

from __future__ import annotations


# --- assimilated symbol ---
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

