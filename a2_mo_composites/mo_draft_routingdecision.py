# Extracted from C:/!ass-ade/src/ass_ade/agent/routing.py:87
# Component id: mo.source.ass_ade.routingdecision
from __future__ import annotations

__version__ = "0.1.0"

class RoutingDecision:
    """Result of an epistemic routing decision."""

    tier: ModelTier
    complexity: float  # ∈ [0, 1]
    recommended_model: str | None = None
    reason: str = ""
    source: str = "local"  # "local" | "nexus"
