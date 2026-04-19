# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1300
# Component id: mo.source.ass_ade.vanguard_mev_route
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_mev_route(self, agent_id: str, intent: dict | None = None, **kwargs: Any) -> VanguardMevRouteResult:
    """POST /v1/vanguard/mev/route-intent — MEV route governance. $0.040/call"""
    return self._post_model("/v1/vanguard/mev/route-intent", VanguardMevRouteResult, {"agent_id": agent_id, "intent": intent or {}, **kwargs})
