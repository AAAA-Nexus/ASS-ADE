# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:553
# Component id: mo.source.ass_ade.spendingbudgetresult
from __future__ import annotations

__version__ = "0.1.0"

class SpendingBudgetResult(NexusModel):
    """/v1/spending/budget — SPG-101"""
    within_budget: bool | None = None
    total_spend_usdc: float | None = None
    per_hop: list[dict] = Field(default_factory=list)
