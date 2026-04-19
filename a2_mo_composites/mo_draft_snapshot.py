# Extracted from C:/!ass-ade/src/ass_ade/tools/history.py:27
# Component id: mo.source.ass_ade.snapshot
from __future__ import annotations

__version__ = "0.1.0"

class Snapshot:
    """A recorded file state before a mutation."""

    path: str
    sequence: int
    timestamp: float
    content: str
