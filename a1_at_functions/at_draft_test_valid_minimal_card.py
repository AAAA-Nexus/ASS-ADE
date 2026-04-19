# Extracted from C:/!ass-ade/tests/test_a2a.py:26
# Component id: at.source.ass_ade.test_valid_minimal_card
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_minimal_card(self) -> None:
    data = {"name": "TestAgent"}
    report = validate_agent_card(data)
    assert report.valid
    assert report.card is not None
    assert report.card.name == "TestAgent"
