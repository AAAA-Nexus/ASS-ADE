# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:818
# Component id: mo.source.a2_mo_composites.defi_liquidation_check
from __future__ import annotations

__version__ = "0.1.0"

def defi_liquidation_check(self, position: dict | None = None, **kwargs: Any) -> LiquidationCheck:
    """/v1/defi/liquidation-check — health factor + time-to-liquidation (LQS-100). $0.04 + 1% equity"""
    resolved_position = position or {
        "position_id": kwargs.pop("position_id", None),
        "collateral_value": kwargs.pop("collateral_value", None),
        "debt_value": kwargs.pop("debt_value", None),
        "collateral_factor": kwargs.pop("collateral_factor", None),
    }
    return self._post_model("/v1/defi/liquidation-check", LiquidationCheck, {"position": resolved_position, **kwargs})
