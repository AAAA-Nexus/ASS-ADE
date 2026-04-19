# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:262
# Component id: mo.source.ass_ade.escrowcreated
from __future__ import annotations

__version__ = "0.1.0"

class EscrowCreated(NexusModel):
    """/v1/escrow/create"""
    escrow_id: str | None = None
    amount_usdc: float | None = None
    status: str | None = None
    release_conditions: list[str] = Field(default_factory=list)
    expires_at: str | None = None
