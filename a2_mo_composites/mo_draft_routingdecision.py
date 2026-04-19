# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_routingdecision.py:7
# Component id: mo.source.a2_mo_composites.routingdecision
from __future__ import annotations

__version__ = "0.1.0"

class RoutingDecision:
    """Result of an epistemic routing decision."""

    tier: ModelTier
    complexity: float  # ∈ [0, 1]
    recommended_model: str | None = None
    reason: str = ""
    source: str = "local"  # "local" | "nexus"
