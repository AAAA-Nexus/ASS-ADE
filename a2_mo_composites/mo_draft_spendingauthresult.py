# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:546
# Component id: mo.source.ass_ade.spendingauthresult
from __future__ import annotations

__version__ = "0.1.0"

class SpendingAuthResult(NexusModel):
    """/v1/spending/authorize — SPG-100"""
    approved: bool | None = None
    approved_amount_usdc: float | None = None
    tau_trust_decay: float | None = None
