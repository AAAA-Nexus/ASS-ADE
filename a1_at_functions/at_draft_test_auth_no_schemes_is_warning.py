# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_auth_no_schemes_is_warning.py:7
# Component id: at.source.a1_at_functions.test_auth_no_schemes_is_warning
from __future__ import annotations

__version__ = "0.1.0"

def test_auth_no_schemes_is_warning(self) -> None:
    data = {"name": "TestAgent", "authentication": {"schemes": []}}
    report = validate_agent_card(data)
    assert any(i.severity == "warning" and "schemes" in i.field for i in report.issues)
