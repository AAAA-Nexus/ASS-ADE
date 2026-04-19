# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testpaymentproof.py:50
# Component id: qk.source.a0_qk_constants.test_header_roundtrip
from __future__ import annotations

__version__ = "0.1.0"

def test_header_roundtrip(self) -> None:
    """PaymentProof should roundtrip through header format."""
    original = PaymentProof(
        signature="sig456",
        wallet_address="0xabcdef",
        transaction_id="0x9876",
        amount_micro_usdc=5000,
    )
    header = original.to_header_value()
    restored = PaymentProof.from_header_value(header)
    assert restored == original
