"""Tier a1 — assimilated function 'extract_symbols'

Assimilated from: rebuild/project_parser.py:187-202
"""

from __future__ import annotations


# --- assimilated symbol ---
def extract_symbols(path: Path) -> list[Symbol]:
    text = _read_text(path)
    if text is None:
        return []
    suffix = path.suffix.lower()
    if suffix == ".py":
        return _extract_python_symbols(path, text)
    if suffix in {".ts", ".tsx", ".js", ".jsx"}:
        return _extract_regex_symbols(path, text, "typescript", TS_SYMBOL_PATTERNS)
    if suffix == ".rs":
        return _extract_regex_symbols(path, text, "rust", RS_SYMBOL_PATTERNS)
    if suffix == ".kt":
        return _extract_regex_symbols(path, text, "kotlin", KT_SYMBOL_PATTERNS)
    if suffix == ".swift":
        return _extract_regex_symbols(path, text, "swift", SWIFT_SYMBOL_PATTERNS)
    return []

