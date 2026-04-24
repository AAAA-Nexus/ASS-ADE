"""Tier a2 — assimilated class 'ToolCallRequest'

Assimilated from: types_llm.py:10-15
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# --- assimilated symbol ---
class ToolCallRequest(BaseModel):
    """A tool invocation requested by a model."""

    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)

