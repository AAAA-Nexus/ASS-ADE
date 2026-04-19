# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:324
# Component id: mo.source.ass_ade.slaresult
__version__ = "0.1.0"

class SlaResult(NexusModel):
    """Generic for report/breach"""
    sla_id: str | None = None
    compliant: bool | None = None
    penalty_usdc: float | None = None
    message: str | None = None
