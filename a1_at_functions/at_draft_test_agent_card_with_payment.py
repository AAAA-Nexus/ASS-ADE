# Extracted from C:/!ass-ade/tests/test_a2a.py:302
# Component id: at.source.ass_ade.test_agent_card_with_payment
from __future__ import annotations

__version__ = "0.1.0"

def test_agent_card_with_payment(self) -> None:
    card = A2AAgentCard(name="Paid", payment={"type": "x402"})
    assert card.payment == {"type": "x402"}
