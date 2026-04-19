# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentcard.py:38
# Component id: at.source.a1_at_functions.test_missing_name_is_error
from __future__ import annotations

__version__ = "0.1.0"

def test_missing_name_is_error(self) -> None:
    data = {"description": "no name"}
    report = validate_agent_card(data)
    assert not report.valid
    assert any(i.severity == "error" for i in report.issues)
