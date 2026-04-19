# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:298
# Component id: at.source.ass_ade.test_agent_card_name_validation
__version__ = "0.1.0"

    def test_agent_card_name_validation(self) -> None:
        with pytest.raises(Exception):
            A2AAgentCard(name="")
