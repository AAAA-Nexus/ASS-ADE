# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentcard.py:47
# Component id: at.source.ass_ade.test_missing_description_is_warning
__version__ = "0.1.0"

    def test_missing_description_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0"}
        report = validate_agent_card(data)
        assert report.valid
        assert any(i.severity == "warning" and i.field == "description" for i in report.issues)
