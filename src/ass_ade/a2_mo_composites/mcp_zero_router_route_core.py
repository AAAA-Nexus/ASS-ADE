"""Tier a2 — assimilated method 'MCPZeroRouter.route'

Assimilated from: zero_router.py:45-47
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# --- assimilated symbol ---
def route(self, capability_str: str) -> ToolRef | None:
    candidates = self.discover(capability_str, k=1)
    return candidates[0] if candidates else None

