"""Tier a2 — assimilated method 'MCPZeroRouter.run'

Assimilated from: zero_router.py:49-53
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# --- assimilated symbol ---
def run(self, ctx: dict) -> dict:
    cap = ctx.get("capability", "")
    k = int(ctx.get("k", 5))
    tools = self.discover(cap, k)
    return {"tools": [{"name": t.name, "score": t.score, "server": t.server} for t in tools]}

