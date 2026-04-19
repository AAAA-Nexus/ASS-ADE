# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1027
# Component id: mo.source.ass_ade.vanguardescrowresult
__version__ = "0.1.0"

class VanguardEscrowResult(NexusModel):
    """POST /v1/vanguard/escrow/lock-and-verify"""
    lock_id: str | None = None
    verified: bool | None = None
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None
