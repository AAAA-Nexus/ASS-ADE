# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:339
# Component id: mo.source.a2_mo_composites.escrow_create
from __future__ import annotations

__version__ = "0.1.0"

def escrow_create(self, amount_usdc: float, sender: str, receiver: str, conditions: list[str], **kwargs: Any) -> EscrowCreated:
    """/v1/escrow/create — lock USDC with release conditions. $0.040/call"""
    return self._post_model("/v1/escrow/create", EscrowCreated, {
        "amount_usdc": amount_usdc, "sender": sender, "receiver": receiver,
        "conditions": conditions, **kwargs,
    })
