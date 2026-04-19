# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentcard.py:49
# Component id: at.source.a1_at_functions.test_missing_description_is_warning
from __future__ import annotations

__version__ = "0.1.0"

def test_missing_description_is_warning(self) -> None:
    data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0"}
    report = validate_agent_card(data)
    assert report.valid
    assert any(i.severity == "warning" and i.field == "description" for i in report.issues)
