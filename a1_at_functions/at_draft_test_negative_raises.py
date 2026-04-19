# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateusdcamount.py:14
# Component id: at.source.ass_ade.test_negative_raises
__version__ = "0.1.0"

    def test_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            validate_usdc_amount(-5.0)
