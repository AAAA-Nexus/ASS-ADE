# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateusdcamount.py:18
# Component id: at.source.ass_ade.test_too_large_raises
__version__ = "0.1.0"

    def test_too_large_raises(self) -> None:
        with pytest.raises(ValueError, match="maximum"):
            validate_usdc_amount(1_000_001.0)
