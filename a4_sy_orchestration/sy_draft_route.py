# Extracted from C:/!ass-ade/src/ass_ade/mcp/zero_router.py:45
# Component id: sy.source.ass_ade.route
from __future__ import annotations

__version__ = "0.1.0"

def route(self, capability_str: str) -> ToolRef | None:
    candidates = self.discover(capability_str, k=1)
    return candidates[0] if candidates else None
