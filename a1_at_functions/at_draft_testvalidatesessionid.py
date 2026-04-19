# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidatesessionid.py:5
# Component id: at.source.ass_ade.testvalidatesessionid
__version__ = "0.1.0"

class TestValidateSessionId:
    def test_valid(self) -> None:
        assert validate_session_id("sess-abc-123") == "sess-abc-123"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_session_id("")

    def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds 256"):
            validate_session_id("x" * 257)
