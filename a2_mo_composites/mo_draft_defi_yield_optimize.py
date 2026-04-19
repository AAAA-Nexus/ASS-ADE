# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:845
# Component id: mo.source.a2_mo_composites.defi_yield_optimize
from __future__ import annotations

__version__ = "0.1.0"

def defi_yield_optimize(
    self,
    capital_usdc: float | None = None,
    protocols: list[str] | None = None,
    *,
    amount_usdc: float | None = None,
    risk_tolerance: str | None = None,
    **kwargs: Any,
) -> YieldOptimize:
    """/v1/defi/yield-optimize — optimal yield allocation (YLD-100). $0.04 + 2% alpha"""
    resolved_capital = capital_usdc if capital_usdc is not None else amount_usdc or 0.0
    resolved_protocols = protocols or []
    if risk_tolerance is not None:
        kwargs.setdefault("risk_tolerance", risk_tolerance)
    return self._post_model("/v1/defi/yield-optimize", YieldOptimize, {
        "capital_usdc": resolved_capital, "protocols": resolved_protocols, **kwargs,
    })
