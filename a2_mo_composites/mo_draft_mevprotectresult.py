# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_mevprotectresult.py:7
# Component id: mo.source.a2_mo_composites.mevprotectresult
from __future__ import annotations

__version__ = "0.1.0"

class MevProtectResult(NexusModel):
    """POST /v1/mev/protect (MEV-100)"""
    bundle_id: str | None = None
    protected: bool | None = None
    strategy: str | None = None
    estimated_mev_saved_usd: float | None = None
    submission_time_ms: int | None = None
