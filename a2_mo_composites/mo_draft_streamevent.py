# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/loop.py:41
# Component id: mo.source.ass_ade.streamevent
__version__ = "0.1.0"

class StreamEvent:
    """An event emitted during streaming agent execution."""

    kind: Literal["token", "tool_call", "tool_result", "blocked", "done", "error"]
    text: str = ""
    tool_name: str = ""
    tool_args: dict[str, Any] = field(default_factory=dict)
    tool_result: ToolResult | None = None
