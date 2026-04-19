# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1087
# Component id: mo.source.ass_ade.forgedeltasubmitresult
from __future__ import annotations

__version__ = "0.1.0"

class ForgeDeltaSubmitResult(NexusModel):
    """POST /v1/forge/delta/submit"""
    submission_id: str | None = None
    accepted: bool | None = None
    delta_score: float | None = None
    reward_usdc: float | None = None
