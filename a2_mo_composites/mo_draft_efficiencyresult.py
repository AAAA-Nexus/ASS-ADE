# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:878
# Component id: mo.source.ass_ade.efficiencyresult
from __future__ import annotations

__version__ = "0.1.0"

class EfficiencyResult(NexusModel):
    """/v1/efficiency — PAY-506"""
    roi_signal: float | None = None
    interactions_analysed: int | None = None
    efficiency_score: float | None = None
