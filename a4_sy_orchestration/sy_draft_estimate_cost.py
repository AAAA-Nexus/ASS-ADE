# Extracted from C:/!ass-ade/src/ass_ade/mcp/utils.py:122
# Component id: sy.source.ass_ade.estimate_cost
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
