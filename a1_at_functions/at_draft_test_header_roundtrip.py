# Extracted from C:/!ass-ade/tests/test_x402_flow.py:131
# Component id: at.source.ass_ade.test_header_roundtrip
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
