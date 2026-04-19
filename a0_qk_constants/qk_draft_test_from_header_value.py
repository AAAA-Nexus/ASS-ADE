# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testpaymentproof.py:38
# Component id: qk.source.ass_ade.test_from_header_value
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
