# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/types.py:36
# Component id: mo.source.ass_ade.completionrequest
__version__ = "0.1.0"

class CompletionRequest(BaseModel):
    """Model completion request."""

    messages: list[Message]
    tools: list[ToolSchema] = Field(default_factory=list)
    temperature: float = 0.0
    max_tokens: int = 4096
    model: str | None = None
