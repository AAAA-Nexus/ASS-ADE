# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:278
# Component id: mo.source.ass_ade.escrowresult
__version__ = "0.1.0"

class EscrowResult(NexusModel):
    """Generic for release / dispute / arbitrate"""
    escrow_id: str | None = None
    status: str | None = None
    message: str | None = None
