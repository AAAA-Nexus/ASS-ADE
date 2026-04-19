# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentid.py:26
# Component id: at.source.ass_ade.test_invalid_chars_raises
__version__ = "0.1.0"

    def test_invalid_chars_raises(self) -> None:
        with pytest.raises(ValueError, match="invalid characters"):
            validate_agent_id("agent id with spaces")
        with pytest.raises(ValueError, match="invalid characters"):
            validate_agent_id("agent<script>")
