# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:738
# Component id: mo.source.ass_ade.liquidationcheck
from __future__ import annotations

__version__ = "0.1.0"

class LiquidationCheck(NexusModel):
    """/v1/defi/liquidation-check — LQS-100"""
    health_factor: float | None = None
    time_to_liquidation_s: int | None = None
    recommended_top_up_usdc: float | None = None
