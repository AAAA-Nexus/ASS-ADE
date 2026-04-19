# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_valid_minimal_card.py:7
# Component id: at.source.a1_at_functions.test_valid_minimal_card
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_minimal_card(self) -> None:
    data = {"name": "TestAgent"}
    report = validate_agent_card(data)
    assert report.valid
    assert report.card is not None
    assert report.card.name == "TestAgent"
