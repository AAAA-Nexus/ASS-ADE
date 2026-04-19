# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_trustdecayresult.py:7
# Component id: mo.source.a2_mo_composites.trustdecayresult
from __future__ import annotations

__version__ = "0.1.0"

class TrustDecayResult(NexusModel):
    """/v1/trust/decay"""
    decayed_score: float | None = None
    original_score: float | None = None
    epochs_elapsed: int | None = None
