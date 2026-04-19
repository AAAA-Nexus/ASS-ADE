# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/project_parser.py:120
# Component id: at.source.ass_ade.extract_symbols
from __future__ import annotations

__version__ = "0.1.0"

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
    return []
