# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:145
# Component id: mo.source.ass_ade.entropyresult
from __future__ import annotations

__version__ = "0.1.0"

class EntropyResult(NexusModel):
    """/v1/oracle/entropy"""
    entropy_bits: float | None = None
    epoch: int | None = None
    verdict: str | None = None
