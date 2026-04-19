# Extracted from C:/!ass-ade/src/ass_ade/system.py:9
# Component id: sy.source.ass_ade.toolstatus
from __future__ import annotations

__version__ = "0.1.0"

class ToolStatus:
    name: str
    available: bool
    version: str | None = None
    error: str | None = None
