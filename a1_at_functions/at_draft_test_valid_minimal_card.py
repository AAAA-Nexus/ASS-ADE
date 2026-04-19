# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:26
# Component id: at.source.ass_ade.test_valid_minimal_card
__version__ = "0.1.0"

    def test_valid_minimal_card(self) -> None:
        data = {"name": "TestAgent"}
        report = validate_agent_card(data)
        assert report.valid
        assert report.card is not None
        assert report.card.name == "TestAgent"
