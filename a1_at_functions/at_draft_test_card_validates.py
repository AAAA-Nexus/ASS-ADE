# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_card_validates.py:7
# Component id: at.source.a1_at_functions.test_card_validates
from __future__ import annotations

__version__ = "0.1.0"

def test_card_validates(self) -> None:
    card = local_agent_card(".")
    report = validate_agent_card(card.model_dump())
    # Should be valid (may have warnings but no errors)
    assert not report.errors
