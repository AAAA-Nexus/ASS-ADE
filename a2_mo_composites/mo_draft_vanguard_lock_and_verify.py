# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:1117
# Component id: mo.source.a2_mo_composites.vanguard_lock_and_verify
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_lock_and_verify(
    self,
    payer_agent_id: str | None = None,
    payee_agent_id: str | None = None,
    amount_micro_usdc: int | None = None,
    *,
    agent_id: str | None = None,
    amount_usdc: float | None = None,
    **kwargs: Any,
) -> VanguardEscrowResult:
    """POST /v1/vanguard/escrow/lock-and-verify — lock + verify escrow (Vanguard). $0.040/call"""
    resolved_payer = payer_agent_id or agent_id or ""
    resolved_payee = payee_agent_id or agent_id or ""
    resolved_amount = amount_micro_usdc
    if resolved_amount is None:
        resolved_amount = int((amount_usdc or 0.0) * 1_000_000)
    return self._post_model("/v1/vanguard/escrow/lock-and-verify", VanguardEscrowResult, {
        "payer_agent_id": resolved_payer,
        "payee_agent_id": resolved_payee,
        "amount_micro_usdc": resolved_amount,
        **kwargs,
    })
