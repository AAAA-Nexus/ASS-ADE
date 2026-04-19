# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:391
# Component id: mo.source.ass_ade.contradictionresult
from __future__ import annotations

__version__ = "0.1.0"

class ContradictionResult(NexusModel):
    """/v1/agents/contradiction"""
    contradicts: bool | None = None
    confidence: float | None = None
    explanation: str | None = None
