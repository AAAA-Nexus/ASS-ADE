# Extracted from C:/!ass-ade/tests/test_x402_flow.py:121
# Component id: at.source.ass_ade.test_from_header_value
from __future__ import annotations

__version__ = "0.1.0"

def test_from_header_value(self) -> None:
    """PaymentProof should parse from HTTP header value."""
    header = "sig123;0x1234;0xabc;8000"
    proof = PaymentProof.from_header_value(header)
    assert proof is not None
    assert proof.signature == "sig123"
    assert proof.wallet_address == "0x1234"
    assert proof.transaction_id == "0xabc"
    assert proof.amount_micro_usdc == 8000
