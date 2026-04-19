# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_mcptool.py:5
# Component id: sy.source.ass_ade.mcptool
__version__ = "0.1.0"

class MCPTool(NexusModel):
    name: str | None = None
    endpoint: str | None = None
    method: str | None = None
    paid: bool | None = None
    inputSchema: dict | None = Field(default=None)
    cost: CostEstimate | None = None
