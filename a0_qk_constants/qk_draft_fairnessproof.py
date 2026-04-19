# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_fairnessproof.py:5
# Component id: qk.source.ass_ade.fairnessproof
__version__ = "0.1.0"

class FairnessProof(NexusModel):
    """/v1/compliance/fairness — FNS-100"""
    disparate_impact_ratio: float | None = None
    within_bound: bool | None = None
    theorem: str | None = None   # "FNS-100-FairnessBound"
