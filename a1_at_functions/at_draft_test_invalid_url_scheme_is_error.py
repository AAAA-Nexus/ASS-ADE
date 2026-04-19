# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_testvalidateagentcard.py:59
# Component id: at.source.ass_ade.test_invalid_url_scheme_is_error
__version__ = "0.1.0"

    def test_invalid_url_scheme_is_error(self) -> None:
        data = {"name": "TestAgent", "url": "ftp://bad.com"}
        report = validate_agent_card(data)
        assert not report.valid
        assert any("scheme" in i.message for i in report.errors)
