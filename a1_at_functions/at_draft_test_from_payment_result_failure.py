# Extracted from C:/!ass-ade/tests/test_x402_flow.py:104
# Component id: at.source.ass_ade.test_from_payment_result_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_from_payment_result_failure(self) -> None:
    """PaymentProof should return None for failed PaymentResult."""
    result = PaymentResult(success=False, error="No wallet")
    proof = PaymentProof.from_payment_result(result)
    assert proof is None
