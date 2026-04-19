# Extracted from C:/!ass-ade/tests/test_a2a.py:67
# Component id: at.source.ass_ade.test_missing_description_is_warning
from __future__ import annotations

__version__ = "0.1.0"

def test_missing_description_is_warning(self) -> None:
    data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0"}
    report = validate_agent_card(data)
    assert report.valid
    assert any(i.severity == "warning" and i.field == "description" for i in report.issues)
