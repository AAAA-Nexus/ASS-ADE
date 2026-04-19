# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentcard.py:61
# Component id: at.source.a1_at_functions.test_invalid_url_scheme_is_error
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_url_scheme_is_error(self) -> None:
    data = {"name": "TestAgent", "url": "ftp://bad.com"}
    report = validate_agent_card(data)
    assert not report.valid
    assert any("scheme" in i.message for i in report.errors)
