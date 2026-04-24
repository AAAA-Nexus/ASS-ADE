"""Tier a1 — pure helpers for symbol extraction, tier mapping, and file composition."""

from __future__ import annotations

import re
from pathlib import Path

_KIND_TO_TIER: dict[str, str] = {
    "function": "a1_at_functions",
    "class": "a2_mo_composites",
    "method": "a2_mo_composites",
}

_TIER_NAMING_SUFFIX: dict[str, str] = {
    "a1_at_functions": "helpers",
    "a2_mo_composites": "core",
    "a3_og_features": "feature",
    "a4_sy_orchestration": "main",
}


def tier_for_kind(kind: str, override: str | None = None) -> str:
    """Map a symbol kind to its canonical monadic tier directory name."""
    if override:
        return override
    return _KIND_TO_TIER.get(kind, "a2_mo_composites")


def slugify_qualname(qualname: str) -> str:
    """Convert a qualname to a snake_case filesystem slug.

    'MyClass.my_method' → 'my_class_my_method'
    """
    # Split on dots (class.method separator)
    parts = qualname.split(".")
    slugs: list[str] = []
    for part in parts:
        # Insert underscore before uppercase sequences (CamelCase → snake_case)
        s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", part)
        s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
        slugs.append(s.lower())
    return "_".join(slugs)


def suggest_target_filename(qualname: str, kind: str, tier: str) -> str:
    """Suggest a target filename for an assimilated symbol.

    Examples:
        ('my_util_fn', 'function', 'a1_at_functions')  → 'my_util_fn_helpers.py'
        ('MyClient', 'class', 'a2_mo_composites')      → 'my_client_core.py'
    """
    suffix = _TIER_NAMING_SUFFIX.get(tier, "assimilated")
    slug = slugify_qualname(qualname)
    return f"{slug}_{suffix}.py"


def extract_source_lines(source_path: str | Path, lineno: int, end_lineno: int) -> str:
    """Extract raw source lines [lineno, end_lineno] (1-based, inclusive)."""
    path = Path(source_path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return f"# ERROR: could not read {source_path}: {exc}\n"
    lines = text.splitlines(keepends=True)
    start = max(0, lineno - 1)
    end = min(len(lines), end_lineno)
    return "".join(lines[start:end])


def extract_module_imports(source_path: str | Path, max_lines: int = 60) -> str:
    """Extract the import block (top of file) so assimilated symbols stay portable."""
    path = Path(source_path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    import_lines: list[str] = []
    for line in text.splitlines()[:max_lines]:
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")) or stripped == "":
            import_lines.append(line)
        elif import_lines and not stripped.startswith(("#", "from __future__")):
            # Stop at first non-import non-blank line after imports started
            if stripped and not stripped.startswith("import") and not stripped.startswith("from"):
                break
    return "\n".join(import_lines).strip()


def compose_file_header(tier: str, description: str, source_ref: str) -> str:
    """Generate the standard header for a new assimilated file."""
    return (
        f'"""Tier {tier[:2]} — {description}\n\n'
        f"Assimilated from: {source_ref}\n"
        '"""\n\n'
        "from __future__ import annotations\n"
    )


def count_loc(source: str) -> int:
    """Count non-blank, non-comment lines."""
    return sum(
        1
        for line in source.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )
