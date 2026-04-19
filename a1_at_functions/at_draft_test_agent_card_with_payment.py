# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testmodels.py:10
# Component id: at.source.ass_ade.test_agent_card_with_payment
__version__ = "0.1.0"

    def test_agent_card_with_payment(self) -> None:
        card = A2AAgentCard(name="Paid", payment={"type": "x402"})
        assert card.payment == {"type": "x402"}
