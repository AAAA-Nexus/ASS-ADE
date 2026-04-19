# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:152
# Component id: mo.source.ass_ade.trustdecayresult
from __future__ import annotations

__version__ = "0.1.0"

class TrustDecayResult(NexusModel):
    """/v1/trust/decay"""
    decayed_score: float | None = None
    original_score: float | None = None
    epochs_elapsed: int | None = None
