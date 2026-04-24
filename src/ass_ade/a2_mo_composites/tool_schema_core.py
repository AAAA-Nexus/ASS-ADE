"""Tier a2 — assimilated class 'ToolSchema'

Assimilated from: types_llm.py:28-33
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# --- assimilated symbol ---
class ToolSchema(BaseModel):
    """Describes a tool the model may invoke."""

    name: str
    description: str
    parameters: dict[str, Any]

