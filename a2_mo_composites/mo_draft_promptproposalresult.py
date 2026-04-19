# Extracted from C:/!ass-ade/src/ass_ade/prompt_toolkit.py:64
# Component id: mo.source.ass_ade.promptproposalresult
from __future__ import annotations

__version__ = "0.1.0"

class PromptProposalResult(BaseModel):
    proposal_id: str
    source: str
    prompt_sha256: str
    objective: str
    recommended_changes: list[str]
    verification_criteria: list[str]
    requires_human_approval: bool = True
    next_action: str
