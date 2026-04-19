# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testraiseforstatus.py:19
# Component id: at.source.ass_ade.test_402_raises_payment_required
__version__ = "0.1.0"

    def test_402_raises_payment_required(self) -> None:
        with pytest.raises(NexusPaymentRequired) as exc_info:
            raise_for_status(402, endpoint="/v1/inference")
        assert exc_info.value.status_code == 402
