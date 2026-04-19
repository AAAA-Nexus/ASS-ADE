# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testpaymentproof.py:29
# Component id: qk.source.a0_qk_constants.test_to_header_value
from __future__ import annotations

__version__ = "0.1.0"

def test_to_header_value(self) -> None:
    """PaymentProof should format as HTTP header value."""
    proof = PaymentProof(
        signature="sig123",
        wallet_address="0x1234",
        transaction_id="0xabc",
        amount_micro_usdc=8000,
    )
    header = proof.to_header_value()
    assert header == "sig123;0x1234;0xabc;8000"
