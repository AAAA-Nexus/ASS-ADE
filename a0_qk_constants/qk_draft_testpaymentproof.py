# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testpaymentproof.py:7
# Component id: qk.source.a0_qk_constants.testpaymentproof
from __future__ import annotations

__version__ = "0.1.0"

class TestPaymentProof:
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

    def test_from_payment_result_failure(self) -> None:
        """PaymentProof should return None for failed PaymentResult."""
        result = PaymentResult(success=False, error="No wallet")
        proof = PaymentProof.from_payment_result(result)
        assert proof is None

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

    def test_from_header_value(self) -> None:
        """PaymentProof should parse from HTTP header value."""
        header = "sig123;0x1234;0xabc;8000"
        proof = PaymentProof.from_header_value(header)
        assert proof is not None
        assert proof.signature == "sig123"
        assert proof.wallet_address == "0x1234"
        assert proof.transaction_id == "0xabc"
        assert proof.amount_micro_usdc == 8000

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
