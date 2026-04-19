# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_vanguardmevrouteresult.py:7
# Component id: sy.source.a4_sy_orchestration.vanguardmevrouteresult
from __future__ import annotations

__version__ = "0.1.0"

class VanguardMevRouteResult(NexusModel):
    """POST /v1/vanguard/mev/route-intent"""
    route_id: str | None = None
    approved: bool | None = None
    priority_score: float | None = None
    estimated_mev_usd: float | None = None
    slippage_within_tolerance: bool | None = None
