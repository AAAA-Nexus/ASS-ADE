# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateusdcamount.py:10
# Component id: at.source.ass_ade.test_zero_raises
__version__ = "0.1.0"

    def test_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            validate_usdc_amount(0.0)
