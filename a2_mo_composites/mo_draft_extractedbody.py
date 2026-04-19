# Extracted from C:/!ass-ade/src/ass_ade/engine/rebuild/body_extractor.py:20
# Component id: mo.source.ass_ade.extractedbody
from __future__ import annotations

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
