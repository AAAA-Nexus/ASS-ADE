# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_promptsectionresult.py:7
# Component id: mo.source.a2_mo_composites.promptsectionresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptSectionResult(BaseModel):
    source: str
    section: str
    found: bool
    text: str = ""
    sha256: str | None = None
