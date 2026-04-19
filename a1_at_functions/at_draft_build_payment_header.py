# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_build_payment_header.py:7
# Component id: at.source.a1_at_functions.build_payment_header
from __future__ import annotations

__version__ = "0.1.0"

def build_payment_header(result: PaymentResult) -> dict[str, str]:
    """Build the HTTP headers to submit with the paid request retry.

    Uses PaymentProof to format the PAYMENT-SIGNATURE header consistently.
    Returns empty dict if payment was unsuccessful.
    """
    proof = PaymentProof.from_payment_result(result)
    if not proof:
        return {}
    return {"PAYMENT-SIGNATURE": proof.to_header_value()}
