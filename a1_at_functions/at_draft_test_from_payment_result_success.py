# Extracted from C:/!ass-ade/tests/test_x402_flow.py:89
# Component id: at.source.ass_ade.test_from_payment_result_success
from __future__ import annotations

__version__ = "0.1.0"

def test_from_payment_result_success(self) -> None:
    """PaymentProof should parse from a successful PaymentResult."""
    result = PaymentResult(
        success=True,
        txid="0xabc123",
        signature_header="sig123;0x1234567890abcdef;0xabc123;8000",
        testnet=True,
    )
    proof = PaymentProof.from_payment_result(result)
    assert proof is not None
    assert proof.signature == "sig123"
    assert proof.wallet_address == "0x1234567890abcdef"
    assert proof.transaction_id == "0xabc123"
    assert proof.amount_micro_usdc == 8000
