# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:1047
# Component id: mo.source.ass_ade.mevstatusresult
from __future__ import annotations

__version__ = "0.1.0"

class MevStatusResult(NexusModel):
    """GET /v1/mev/status (MEV-101)"""
    bundle_id: str | None = None
    status: str | None = None   # "pending" | "submitted" | "confirmed" | "failed"
    included_in_block: int | None = None
    mev_saved_usd: float | None = None
