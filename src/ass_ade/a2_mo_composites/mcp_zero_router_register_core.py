"""Tier a2 — assimilated method 'MCPZeroRouter.register'

Assimilated from: zero_router.py:23-24
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# --- assimilated symbol ---
def register(self, tool: ToolRef) -> None:
    self._catalog.append(tool)

