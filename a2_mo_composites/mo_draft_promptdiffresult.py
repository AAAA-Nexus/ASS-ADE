# Extracted from C:/!ass-ade/src/ass_ade/prompt_toolkit.py:54
# Component id: mo.source.ass_ade.promptdiffresult
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
