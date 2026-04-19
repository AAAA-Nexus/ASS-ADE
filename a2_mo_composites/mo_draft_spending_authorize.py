# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:782
# Component id: mo.source.ass_ade.spending_authorize
from __future__ import annotations

__version__ = "0.1.0"

def spending_authorize(self, agent_id: str, amount_usdc: float, epoch: int = 0, **kwargs: Any) -> SpendingAuthResult:
    """/v1/spending/authorize — trust-decay spending bound (SPG-100). $0.040/call"""
    return self._post_model("/v1/spending/authorize", SpendingAuthResult, {
        "agent_id": agent_id, "amount_usdc": amount_usdc, "epoch": epoch, **kwargs,
    })
