# Extracted from C:/!ass-ade/src/ass_ade/engine/types.py:36
# Component id: mo.source.ass_ade.completionrequest
from __future__ import annotations

__version__ = "0.1.0"

class CompletionRequest(BaseModel):
    """Model completion request."""

    messages: list[Message]
    tools: list[ToolSchema] = Field(default_factory=list)
    temperature: float = 0.0
    max_tokens: int = 4096
    model: str | None = None
