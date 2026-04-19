# Extracted from C:/!ass-ade/src/ass_ade/tools/registry.py:23
# Component id: og.source.ass_ade.get
from __future__ import annotations

__version__ = "0.1.0"

def get(self, name: str) -> Tool | None:
    return self._tools.get(name)
