# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_mevstatusresult.py:7
# Component id: mo.source.a2_mo_composites.mevstatusresult
from __future__ import annotations

__version__ = "0.1.0"

class MevStatusResult(NexusModel):
    """GET /v1/mev/status (MEV-101)"""
    bundle_id: str | None = None
    status: str | None = None   # "pending" | "submitted" | "confirmed" | "failed"
    included_in_block: int | None = None
    mev_saved_usd: float | None = None
