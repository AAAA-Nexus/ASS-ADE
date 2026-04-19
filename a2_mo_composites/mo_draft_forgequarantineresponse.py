# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1079
# Component id: mo.source.ass_ade.forgequarantineresponse
__version__ = "0.1.0"

class ForgeQuarantineResponse(NexusModel):
    """POST /v1/forge/quarantine"""
    quarantined: Any = None
    model_id: str | None = None
    reason: str | None = None
    count: int | None = None
