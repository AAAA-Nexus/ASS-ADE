# Extracted from C:/!ass-ade/src/ass_ade/mcp/zero_router.py:23
# Component id: sy.source.ass_ade.register
from __future__ import annotations

__version__ = "0.1.0"

def register(self, tool: ToolRef) -> None:
    self._catalog.append(tool)
