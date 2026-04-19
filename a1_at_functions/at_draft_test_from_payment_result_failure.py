# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_from_payment_result_failure.py:7
# Component id: at.source.a1_at_functions.test_from_payment_result_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_from_payment_result_failure(self) -> None:
    """PaymentProof should return None for failed PaymentResult."""
    result = PaymentResult(success=False, error="No wallet")
    proof = PaymentProof.from_payment_result(result)
    assert proof is None
