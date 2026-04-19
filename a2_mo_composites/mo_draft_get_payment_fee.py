# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:98
# Component id: mo.source.a2_mo_composites.get_payment_fee
from __future__ import annotations

__version__ = "0.1.0"

def get_payment_fee(self) -> PaymentFee:
    """/v1/payments/fee — current x402 payment requirements, free"""
    return self._get_model("/v1/payments/fee", PaymentFee)
