# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateusdcamount.py:6
# Component id: at.source.ass_ade.test_valid_amounts
__version__ = "0.1.0"

    def test_valid_amounts(self) -> None:
        assert validate_usdc_amount(0.01) == 0.01
        assert validate_usdc_amount(1_000_000.0) == 1_000_000.0
