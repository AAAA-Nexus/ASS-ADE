# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:262
# Component id: mo.source.ass_ade.escrowcreated
__version__ = "0.1.0"

class EscrowCreated(NexusModel):
    """/v1/escrow/create"""
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None
    release_conditions: list[str] = Field(default_factory=list)
    expires_at: str | None = None
