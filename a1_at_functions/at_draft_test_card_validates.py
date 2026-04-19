# Extracted from C:/!ass-ade/tests/test_a2a.py:287
# Component id: at.source.ass_ade.test_card_validates
from __future__ import annotations

__version__ = "0.1.0"

def test_card_validates(self) -> None:
    card = local_agent_card(".")
    report = validate_agent_card(card.model_dump())
    # Should be valid (may have warnings but no errors)
    assert not report.errors
