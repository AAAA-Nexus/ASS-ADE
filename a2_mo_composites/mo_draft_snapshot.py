# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_snapshot.py:7
# Component id: mo.source.a2_mo_composites.snapshot
from __future__ import annotations

__version__ = "0.1.0"

class Snapshot:
    """A recorded file state before a mutation."""

    path: str
    sequence: int
    timestamp: float
    content: str
