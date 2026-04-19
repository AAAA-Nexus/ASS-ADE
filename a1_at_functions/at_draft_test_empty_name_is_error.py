# Extracted from C:/!ass-ade/tests/test_a2a.py:62
# Component id: at.source.ass_ade.test_empty_name_is_error
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_name_is_error(self) -> None:
    data = {"name": "   "}
    report = validate_agent_card(data)
    assert not report.valid
