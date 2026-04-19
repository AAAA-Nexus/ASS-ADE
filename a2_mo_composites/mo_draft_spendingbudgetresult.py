# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_spendingbudgetresult.py:7
# Component id: mo.source.a2_mo_composites.spendingbudgetresult
from __future__ import annotations

__version__ = "0.1.0"

class SpendingBudgetResult(NexusModel):
    """/v1/spending/budget — SPG-101"""
    within_budget: bool | None = None
    total_spend_usdc: float | None = None
    per_hop: list[dict] = Field(default_factory=list)
