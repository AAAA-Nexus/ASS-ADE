# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/types.py:18
# Component id: mo.source.ass_ade.message
__version__ = "0.1.0"

class Message(BaseModel):
    """A single message in a conversation."""

    role: str  # "system" | "user" | "assistant" | "tool"
    content: str = ""
    tool_calls: list[ToolCallRequest] = Field(default_factory=list)
    tool_call_id: str | None = None
    name: str | None = None
