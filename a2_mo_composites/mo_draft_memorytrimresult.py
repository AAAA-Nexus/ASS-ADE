# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_memorytrimresult.py:7
# Component id: mo.source.a2_mo_composites.memorytrimresult
from __future__ import annotations

__version__ = "0.1.0"

class MemoryTrimResult(NexusModel):
    """/v1/memory/trim — INF-815"""
    tokens_before: int | None = None
    tokens_after: int | None = None
    pruned_entries: int | None = None
