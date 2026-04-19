# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentcard.py:42
# Component id: at.source.ass_ade.test_empty_name_is_error
__version__ = "0.1.0"

    def test_empty_name_is_error(self) -> None:
        data = {"name": "   "}
        report = validate_agent_card(data)
        assert not report.valid
