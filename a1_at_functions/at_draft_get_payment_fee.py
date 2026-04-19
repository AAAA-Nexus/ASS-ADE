# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_get_payment_fee.py:7
# Component id: at.source.a1_at_functions.get_payment_fee
from __future__ import annotations

__version__ = "0.1.0"

def get_payment_fee(self) -> PaymentFee:
    """/v1/payments/fee — current x402 payment requirements, free"""
    return self._get_model("/v1/payments/fee", PaymentFee)
