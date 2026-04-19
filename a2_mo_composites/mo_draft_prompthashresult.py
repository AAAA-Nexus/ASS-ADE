# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_prompthashresult.py:7
# Component id: mo.source.a2_mo_composites.prompthashresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptHashResult(BaseModel):
    source: str
    sha256: str
    bytes: int
    lines: int
