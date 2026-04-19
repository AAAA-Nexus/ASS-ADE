# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_promptdiffresult.py:7
# Component id: mo.source.a2_mo_composites.promptdiffresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptDiffResult(BaseModel):
    source: str
    baseline_source: str
    current_sha256: str
    baseline_sha256: str
    diff: str
    redacted: bool = True
    truncated: bool = False
