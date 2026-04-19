# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:293
# Component id: mo.source.ass_ade.get_payment_fee
from __future__ import annotations

__version__ = "0.1.0"

def get_payment_fee(self) -> PaymentFee:
    """/v1/payments/fee — current x402 payment requirements, free"""
    return self._get_model("/v1/payments/fee", PaymentFee)
