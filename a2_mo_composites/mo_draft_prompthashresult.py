# Extracted from C:/!ass-ade/src/ass_ade/prompt_toolkit.py:28
# Component id: mo.source.ass_ade.prompthashresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptHashResult(BaseModel):
    source: str
    sha256: str
    bytes: int
    lines: int
