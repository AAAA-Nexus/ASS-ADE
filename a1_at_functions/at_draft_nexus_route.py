# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/routing.py:133
# Component id: at.source.ass_ade.nexus_route
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
