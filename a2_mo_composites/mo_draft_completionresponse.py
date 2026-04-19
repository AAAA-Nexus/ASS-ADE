# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_completionresponse.py:7
# Component id: mo.source.a2_mo_composites.completionresponse
from __future__ import annotations

__version__ = "0.1.0"

class CompletionResponse(BaseModel):
    """Model completion response."""

    message: Message
    model: str | None = None
    finish_reason: str | None = None  # "stop" | "tool_calls" | "length"
    usage: dict[str, int] | None = None
