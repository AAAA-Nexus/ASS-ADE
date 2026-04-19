# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:803
# Component id: mo.source.a2_mo_composites.defi_risk_score
from __future__ import annotations

__version__ = "0.1.0"

def defi_risk_score(self, protocol: str, position: dict | None = None, **kwargs: Any) -> DefiRiskScore:
    """/v1/defi/risk-score — risk + max drawdown bound 12.5% (DFI-101). $0.08/call"""
    return self._post_model("/v1/defi/risk-score", DefiRiskScore, {"protocol": protocol, "position": position or {}, **kwargs})
