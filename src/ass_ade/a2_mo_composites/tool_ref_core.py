"""Tier a2 — assimilated class 'ToolRef'

Assimilated from: zero_router.py:9-13
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# --- assimilated symbol ---
class ToolRef:
    name: str
    score: float
    server: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

