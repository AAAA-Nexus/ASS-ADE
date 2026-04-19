# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidatesessionid.py:13
# Component id: at.source.ass_ade.test_too_long_raises
__version__ = "0.1.0"

    def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds 256"):
            validate_session_id("x" * 257)
