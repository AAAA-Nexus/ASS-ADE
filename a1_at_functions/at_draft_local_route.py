# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_local_route.py:7
# Component id: at.source.a1_at_functions.local_route
from __future__ import annotations

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
