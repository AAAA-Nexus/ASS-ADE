# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:900
# Component id: mo.source.ass_ade.memorytrimresult
from __future__ import annotations

__version__ = "0.1.0"

class MemoryTrimResult(NexusModel):
    """/v1/memory/trim — INF-815"""
    tokens_before: int | None = None
    tokens_after: int | None = None
    pruned_entries: int | None = None
