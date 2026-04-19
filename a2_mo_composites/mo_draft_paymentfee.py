# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:921
# Component id: mo.source.ass_ade.paymentfee
from __future__ import annotations

__version__ = "0.1.0"

class PaymentFee(NexusModel):
    """/v1/payments/fee — x402 fee oracle"""
    amount: Any = None
    currency: str | None = None
    network: str | None = None
    pay_to: str | None = None
