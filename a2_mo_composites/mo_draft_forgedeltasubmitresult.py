# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_forgedeltasubmitresult.py:7
# Component id: mo.source.a2_mo_composites.forgedeltasubmitresult
from __future__ import annotations

__version__ = "0.1.0"

class ForgeDeltaSubmitResult(NexusModel):
    """POST /v1/forge/delta/submit"""
    submission_id: str | None = None
    accepted: bool | None = None
    delta_score: float | None = None
    reward_usdc: float | None = None
