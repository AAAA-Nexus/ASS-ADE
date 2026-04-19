# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_extract_body.py:7
# Component id: at.source.a1_at_functions.extract_body
from __future__ import annotations

__version__ = "0.1.0"

def extract_body(
    source_path: str | Path, symbol_name: str, language: str = "python"
) -> ExtractedBody | None:
    """Extract the body of one symbol from one source file. Returns None on failure."""
    p = Path(source_path)
    if not p.exists() or p.stat().st_size > _MAX_FILE_BYTES:
        return None
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    if language == "python" or p.suffix == ".py":
        result = _extract_python_body(text, symbol_name)
    else:
        result = _extract_regex_body(text, symbol_name, language)
    if result is not None:
        result.source_path = p.as_posix()
    return result
