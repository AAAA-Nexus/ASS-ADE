# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentcard.py:75
# Component id: at.source.ass_ade.test_skill_missing_id_is_error
__version__ = "0.1.0"

    def test_skill_missing_id_is_error(self) -> None:
        data = {
            "name": "TestAgent",
            "url": "https://example.com",
            "version": "1.0",
            "skills": [{"id": "", "name": "Skill One"}],
        }
        report = validate_agent_card(data)
        assert not report.valid
