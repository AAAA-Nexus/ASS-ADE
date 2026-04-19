# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_x402clientflow.py:93
# Component id: qk.source.a2_mo_composites.get_proof
from __future__ import annotations

__version__ = "0.1.0"

def get_proof(self, payment: PaymentResult) -> PaymentProof | None:
    """Extract structured PaymentProof from a payment result."""
    return PaymentProof.from_payment_result(payment)
