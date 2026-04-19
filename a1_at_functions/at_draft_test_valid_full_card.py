# Extracted from C:/!ass-ade/tests/test_a2a.py:33
# Component id: at.source.ass_ade.test_valid_full_card
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_full_card(self) -> None:
    data = {
        "name": "FullAgent",
        "description": "A complete agent",
        "url": "https://example.com",
        "version": "1.0.0",
        "provider": {"organization": "TestOrg", "url": "https://testorg.com"},
        "capabilities": {"streaming": True, "pushNotifications": False, "stateTransitionHistory": True},
        "authentication": {"schemes": ["bearer"]},
        "skills": [
            {"id": "skill1", "name": "Skill One", "description": "Does things"},
        ],
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain", "application/json"],
    }
    report = validate_agent_card(data)
    assert report.valid
    assert report.card is not None
    assert report.card.name == "FullAgent"
    assert report.card.capabilities.streaming is True
    assert len(report.card.skills) == 1
    assert report.card.skills[0].id == "skill1"
