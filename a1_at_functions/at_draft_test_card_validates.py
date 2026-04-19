# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlocalagentcard.py:13
# Component id: at.source.ass_ade.test_card_validates
__version__ = "0.1.0"

    def test_card_validates(self) -> None:
        card = local_agent_card(".")
        report = validate_agent_card(card.model_dump())
        # Should be valid (may have warnings but no errors)
        assert not report.errors
