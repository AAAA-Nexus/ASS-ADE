# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentcard.py:36
# Component id: at.source.ass_ade.test_missing_name_is_error
__version__ = "0.1.0"

    def test_missing_name_is_error(self) -> None:
        data = {"description": "no name"}
        report = validate_agent_card(data)
        assert not report.valid
        assert any(i.severity == "error" for i in report.issues)
