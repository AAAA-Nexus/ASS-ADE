# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:110
# Component id: at.source.ass_ade.test_to_header_value
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
