# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:83
# Component id: mo.source.ass_ade.costestimate
from __future__ import annotations

__version__ = "0.1.0"

class CostEstimate(NexusModel):
    currency: str = "USDC"
    unit_cost: float | None = None
    rate_limit_rpm: int | None = None
    rate_limit_tpm: int | None = None
    notes: str | None = None
