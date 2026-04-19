# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentcard.py:70
# Component id: at.source.ass_ade.test_no_skills_is_warning
__version__ = "0.1.0"

    def test_no_skills_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0", "description": "desc"}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and i.field == "skills" for i in report.issues)
