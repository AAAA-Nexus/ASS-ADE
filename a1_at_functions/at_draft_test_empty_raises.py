# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentid.py:14
# Component id: at.source.ass_ade.test_empty_raises
__version__ = "0.1.0"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_agent_id("")
