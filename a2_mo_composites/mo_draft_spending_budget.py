# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:593
# Component id: mo.source.a2_mo_composites.spending_budget
from __future__ import annotations

__version__ = "0.1.0"

def spending_budget(
    self,
    chain: list[dict] | None = None,
    total_usdc: float = 0.0,
    *,
    agent_id: str | None = None,
    **kwargs: Any,
) -> SpendingBudgetResult:
    """/v1/spending/budget — multi-hop chain budget (SPG-101). $0.040/call"""
    resolved_chain = chain or ([{"agent_id": agent_id}] if agent_id else [])
    return self._post_model("/v1/spending/budget", SpendingBudgetResult, {"chain": resolved_chain, "total_usdc": total_usdc, **kwargs})
