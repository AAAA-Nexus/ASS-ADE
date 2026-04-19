# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_estimate_cost.py:5
# Component id: at.source.ass_ade.estimate_cost
__version__ = "0.1.0"

def estimate_cost(tool: MCPTool) -> CostEstimate | None:
    """Return the cost metadata for a tool, or None if the tool is free / metadata unavailable."""
    if tool.cost is not None:
        return tool.cost
    if bool(tool.paid):
        # Manifest declares paid but no cost detail; return a placeholder.
        return CostEstimate(notes="paid tool – no cost detail in manifest")
    return None
