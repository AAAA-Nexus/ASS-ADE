# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_trustphaseresult.py:7
# Component id: mo.source.a2_mo_composites.trustphaseresult
from __future__ import annotations

__version__ = "0.1.0"

class TrustPhaseResult(NexusModel):
    """/v1/oracle/v-ai — V_AI phase oracle"""
    phase: float | None = None
    certified: bool | None = None
    monotonicity_preserved: bool | None = None
