# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_extract_body.py:5
# Component id: at.source.ass_ade.extract_body
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
