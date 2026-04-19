# Extracted from C:/!ass-ade/tests/test_a2a.py:56
# Component id: at.source.ass_ade.test_missing_name_is_error
from __future__ import annotations

__version__ = "0.1.0"

def test_missing_name_is_error(self) -> None:
    data = {"description": "no name"}
    report = validate_agent_card(data)
    assert not report.valid
    assert any(i.severity == "error" for i in report.issues)
