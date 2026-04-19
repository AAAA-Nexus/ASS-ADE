# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentcard.py:55
# Component id: at.source.a1_at_functions.test_missing_url_is_warning
from __future__ import annotations

__version__ = "0.1.0"

def test_missing_url_is_warning(self) -> None:
    data = {"name": "TestAgent", "description": "desc"}
    report = validate_agent_card(data)
    assert report.valid
    assert any(i.severity == "warning" and i.field == "url" for i in report.issues)
