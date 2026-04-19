# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentid.py:11
# Component id: at.source.ass_ade.test_strips_whitespace
__version__ = "0.1.0"

    def test_strips_whitespace(self) -> None:
        assert validate_agent_id("  agent-1  ") == "agent-1"
