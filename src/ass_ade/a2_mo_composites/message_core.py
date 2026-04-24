"""Tier a2 — assimilated class 'Message'

Assimilated from: types_llm.py:18-25
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# --- assimilated symbol ---
class Message(BaseModel):
    """A single message in a conversation."""

    role: str  # "system" | "user" | "assistant" | "tool"
    content: str = ""
    tool_calls: list[ToolCallRequest] = Field(default_factory=list)
    tool_call_id: str | None = None
    name: str | None = None

