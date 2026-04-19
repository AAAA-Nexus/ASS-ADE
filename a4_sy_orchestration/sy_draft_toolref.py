# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/mcp/zero_router.py:9
# Component id: sy.source.ass_ade.toolref
__version__ = "0.1.0"

class ToolRef:
    name: str
    score: float
    server: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
