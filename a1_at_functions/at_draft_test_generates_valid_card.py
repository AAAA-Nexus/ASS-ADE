# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:280
# Component id: at.source.ass_ade.test_generates_valid_card
__version__ = "0.1.0"

    def test_generates_valid_card(self, tmp_path: str) -> None:
        card = local_agent_card(str(tmp_path) if isinstance(tmp_path, type(None)) else ".")
        assert card.name == "ASS-ADE"
        assert card.provider is not None
        assert card.provider.organization == "Atomadic"
        assert len(card.skills) > 0
