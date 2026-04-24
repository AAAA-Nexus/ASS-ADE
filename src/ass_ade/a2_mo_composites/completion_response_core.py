"""Tier a2 — assimilated class 'CompletionResponse'

Assimilated from: types_llm.py:46-52
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# --- assimilated symbol ---
class CompletionResponse(BaseModel):
    """Model completion response."""

    message: Message
    model: str | None = None
    finish_reason: str | None = None  # "stop" | "tool_calls" | "length"
    usage: dict[str, int] | None = None

