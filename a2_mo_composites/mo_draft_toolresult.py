# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/tools/base.py:10
# Component id: mo.source.ass_ade.toolresult
__version__ = "0.1.0"

class ToolResult(BaseModel):
    """Result of a tool execution."""

    output: str = ""
    error: str | None = None
    success: bool = True
