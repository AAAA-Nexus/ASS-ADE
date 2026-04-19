# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentcard.py:44
# Component id: at.source.a1_at_functions.test_empty_name_is_error
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_name_is_error(self) -> None:
    data = {"name": "   "}
    report = validate_agent_card(data)
    assert not report.valid
