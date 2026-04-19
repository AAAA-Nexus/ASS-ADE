# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_extractedbody.py:7
# Component id: mo.source.a2_mo_composites.extractedbody
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
