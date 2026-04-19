# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:115
# Component id: at.source.ass_ade.test_auth_no_schemes_is_warning
__version__ = "0.1.0"

    def test_auth_no_schemes_is_warning(self) -> None:
        data = {"name": "TestAgent", "authentication": {"schemes": []}}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and "schemes" in i.field for i in report.issues)
