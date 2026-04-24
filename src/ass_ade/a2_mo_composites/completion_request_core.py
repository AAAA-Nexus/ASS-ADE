"""Tier a2 — assimilated class 'CompletionRequest'

Assimilated from: types_llm.py:36-43
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# --- assimilated symbol ---
class CompletionRequest(BaseModel):
    """Model completion request."""

    messages: list[Message]
    tools: list[ToolSchema] = Field(default_factory=list)
    temperature: float = 0.0
    max_tokens: int = 4096
    model: str | None = None

