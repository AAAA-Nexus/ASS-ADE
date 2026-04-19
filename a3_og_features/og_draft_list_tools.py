# Extracted from C:/!ass-ade/src/ass_ade/tools/registry.py:26
# Component id: og.source.ass_ade.list_tools
from __future__ import annotations

__version__ = "0.1.0"

def list_tools(self) -> list[str]:
    return sorted(self._tools)
