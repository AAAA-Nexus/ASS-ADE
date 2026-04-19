# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:105
# Component id: at.source.ass_ade.test_skill_missing_name_is_error
__version__ = "0.1.0"

    def test_skill_missing_name_is_error(self) -> None:
        data = {
            "name": "TestAgent",
            "url": "https://example.com",
            "version": "1.0",
            "skills": [{"id": "s1", "name": ""}],
        }
        report = validate_agent_card(data)
        assert not report.valid
