# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_entropyresult.py:7
# Component id: mo.source.a2_mo_composites.entropyresult
from __future__ import annotations

__version__ = "0.1.0"

class EntropyResult(NexusModel):
    """/v1/oracle/entropy"""
    entropy_bits: float | None = None
    epoch: int | None = None
    verdict: str | None = None
