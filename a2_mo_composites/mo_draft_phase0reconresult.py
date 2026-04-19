# Extracted from C:/!ass-ade/src/ass_ade/recon.py:110
# Component id: mo.source.ass_ade.phase0reconresult
from __future__ import annotations

__version__ = "0.1.0"

class Phase0ReconResult(BaseModel):
    verdict: ReconVerdict
    task_description: str
    codebase: CodebaseRecon
    research_targets: list[ResearchTarget] = Field(default_factory=list)
    provided_sources: list[str] = Field(default_factory=list)
    required_actions: list[str] = Field(default_factory=list)
    next_action: str
