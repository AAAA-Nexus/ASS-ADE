# Extracted from C:/!ass-ade/src/ass_ade/engine/types.py:46
# Component id: mo.source.ass_ade.completionresponse
from __future__ import annotations

__version__ = "0.1.0"

class CompletionResponse(BaseModel):
    """Model completion response."""

    message: Message
    model: str | None = None
    finish_reason: str | None = None  # "stop" | "tool_calls" | "length"
    usage: dict[str, int] | None = None
