# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/routing.py:119
# Component id: at.source.ass_ade.local_route
__version__ = "0.1.0"

def local_route(message: str) -> RoutingDecision:
    """Route using local heuristics (no Nexus required)."""
    c = classify_complexity(message)
    tier = tier_for_complexity(c)
    candidates = _TIER_MODELS.get(tier, [])
    return RoutingDecision(
        tier=tier,
        complexity=c,
        recommended_model=candidates[0] if candidates else None,
        reason=f"Local heuristic: complexity={c:.2f} → {tier.value}",
        source="local",
    )
