# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_promptproposalresult.py:7
# Component id: mo.source.a2_mo_composites.promptproposalresult
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
