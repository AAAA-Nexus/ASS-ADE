# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpaymentresult.py:12
# Component id: at.source.ass_ade.test_build_header_failure
__version__ = "0.1.0"

    def test_build_header_failure(self) -> None:
        r = PaymentResult(success=False, error="no wallet")
        headers = build_payment_header(r)
        assert headers == {}
