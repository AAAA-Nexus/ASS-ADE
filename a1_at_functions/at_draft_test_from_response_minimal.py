# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpaymentchallenge.py:27
# Component id: at.source.ass_ade.test_from_response_minimal
__version__ = "0.1.0"

    def test_from_response_minimal(self) -> None:
        with pytest.raises(ValueError, match="recipient"):
            PaymentChallenge.from_response({})
