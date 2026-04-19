# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_paymentfee.py:7
# Component id: mo.source.a2_mo_composites.paymentfee
from __future__ import annotations

__version__ = "0.1.0"

class PaymentFee(NexusModel):
    """/v1/payments/fee — x402 fee oracle"""
    amount: Any = None
    currency: str | None = None
    network: str | None = None
    pay_to: str | None = None
