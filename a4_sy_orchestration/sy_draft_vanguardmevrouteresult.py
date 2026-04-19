# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:1010
# Component id: sy.source.ass_ade.vanguardmevrouteresult
__version__ = "0.1.0"

class VanguardMevRouteResult(NexusModel):
    """POST /v1/vanguard/mev/route-intent"""
    route_id: str | None = None
    approved: bool | None = None
    priority_score: float | None = None
    estimated_mev_usd: float | None = None
    slippage_within_tolerance: bool | None = None
