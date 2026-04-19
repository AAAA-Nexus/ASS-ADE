# Extracted from C:/!ass-ade/src/ass_ade/tools/registry.py:20
# Component id: og.source.ass_ade.register
from __future__ import annotations

__version__ = "0.1.0"

def register(self, tool: Tool) -> None:
    self._tools[tool.name] = tool
