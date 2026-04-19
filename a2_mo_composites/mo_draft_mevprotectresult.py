# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1038
# Component id: mo.source.ass_ade.mevprotectresult
__version__ = "0.1.0"

class MevProtectResult(NexusModel):
    """POST /v1/mev/protect (MEV-100)"""
    bundle_id: str | None = None
    protected: bool | None = None
    strategy: str | None = None
    estimated_mev_saved_usd: float | None = None
    submission_time_ms: int | None = None
