# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_message.py:7
# Component id: mo.source.a2_mo_composites.message
from __future__ import annotations

__version__ = "0.1.0"

class Message(BaseModel):
    """A single message in a conversation."""

    role: str  # "system" | "user" | "assistant" | "tool"
    content: str = ""
    tool_calls: list[ToolCallRequest] = Field(default_factory=list)
    tool_call_id: str | None = None
    name: str | None = None
