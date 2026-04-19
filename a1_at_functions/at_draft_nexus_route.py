# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_nexus_route.py:7
# Component id: at.source.a1_at_functions.nexus_route
from __future__ import annotations

__version__ = "0.1.0"

async def nexus_route(
    message: str,
    nexus_client: Any,
    available_models: list[str] | None = None,
) -> RoutingDecision:
    """Route using AAAA-Nexus epistemic routing endpoints.

    Falls back to local routing if Nexus is unavailable.
    """
    try:
        result = nexus_client.routing_recommend(
            prompt=message,
            available_models=available_models or [],
        )
        return RoutingDecision(
            tier=_nexus_tier(result),
            complexity=getattr(result, "complexity", 0.5),
            recommended_model=getattr(result, "recommended_model", None),
            reason=getattr(result, "reason", "Nexus recommendation"),
            source="nexus",
        )
    except Exception:
        return local_route(message)
