# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_promptproposalresult.py:5
# Component id: mo.source.ass_ade.promptproposalresult
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
