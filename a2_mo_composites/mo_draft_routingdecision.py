# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_routingdecision.py:5
# Component id: mo.source.ass_ade.routingdecision
__version__ = "0.1.0"

class RoutingDecision:
    """Result of an epistemic routing decision."""

    tier: ModelTier
    complexity: float  # ∈ [0, 1]
    recommended_model: str | None = None
    reason: str = ""
    source: str = "local"  # "local" | "nexus"
