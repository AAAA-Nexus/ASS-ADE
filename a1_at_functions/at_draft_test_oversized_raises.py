# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateprompt.py:27
# Component id: at.source.ass_ade.test_oversized_raises
__version__ = "0.1.0"

    def test_oversized_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds"):
            validate_prompt("x" * 40_000)
