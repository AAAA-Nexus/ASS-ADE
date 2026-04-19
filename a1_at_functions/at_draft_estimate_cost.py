# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_estimate_cost.py:7
# Component id: at.source.a1_at_functions.estimate_cost
from __future__ import annotations

__version__ = "0.1.0"

def estimate_cost(tool: MCPTool) -> CostEstimate | None:
    """Return the cost metadata for a tool, or None if the tool is free / metadata unavailable."""
    if tool.cost is not None:
        return tool.cost
    if bool(tool.paid):
        # Manifest declares paid but no cost detail; return a placeholder.
        return CostEstimate(notes="paid tool – no cost detail in manifest")
    return None
