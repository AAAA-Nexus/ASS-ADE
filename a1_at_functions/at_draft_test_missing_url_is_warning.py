# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentcard.py:53
# Component id: at.source.ass_ade.test_missing_url_is_warning
__version__ = "0.1.0"

    def test_missing_url_is_warning(self) -> None:
        data = {"name": "TestAgent", "description": "desc"}
        report = validate_agent_card(data)
        assert report.valid
        assert any(i.severity == "warning" and i.field == "url" for i in report.issues)
