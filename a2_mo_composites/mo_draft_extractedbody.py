# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/rebuild/body_extractor.py:19
# Component id: mo.source.ass_ade.extractedbody
__version__ = "0.1.0"

class ExtractedBody:
    source_path: str
    source_line: int
    symbol_name: str
    language: str
    body: str
    imports: list[str]
    callers_of: list[str]
    exceptions_raised: list[str]
