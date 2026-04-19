# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1087
# Component id: mo.source.ass_ade.forgedeltasubmitresult
__version__ = "0.1.0"

class ForgeDeltaSubmitResult(NexusModel):
    """POST /v1/forge/delta/submit"""
    submission_id: str | None = None
    accepted: bool | None = None
    delta_score: float | None = None
    reward_usdc: float | None = None
