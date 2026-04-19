# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testpaymentproof.py:27
# Component id: qk.source.ass_ade.test_to_header_value
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
