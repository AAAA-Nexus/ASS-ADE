# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_contradictionresult.py:7
# Component id: mo.source.a2_mo_composites.contradictionresult
from __future__ import annotations

__version__ = "0.1.0"

class ContradictionResult(NexusModel):
    """/v1/agents/contradiction"""
    contradicts: bool | None = None
    confidence: float | None = None
    explanation: str | None = None
