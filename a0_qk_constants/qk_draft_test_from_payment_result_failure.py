# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_testpaymentproof.py:21
# Component id: qk.source.ass_ade.test_from_payment_result_failure
__version__ = "0.1.0"

    def test_from_payment_result_failure(self) -> None:
        """PaymentProof should return None for failed PaymentResult."""
        result = PaymentResult(success=False, error="No wallet")
        proof = PaymentProof.from_payment_result(result)
        assert proof is None
