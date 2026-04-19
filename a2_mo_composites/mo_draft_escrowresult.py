# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:278
# Component id: mo.source.ass_ade.escrowresult
from __future__ import annotations

__version__ = "0.1.0"

class EscrowResult(NexusModel):
    """Generic for release / dispute / arbitrate"""
    escrow_id: str | None = None
    status: str | None = None
    message: str | None = None
