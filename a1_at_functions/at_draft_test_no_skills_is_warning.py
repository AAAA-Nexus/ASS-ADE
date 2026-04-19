# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_no_skills_is_warning.py:7
# Component id: at.source.a1_at_functions.test_no_skills_is_warning
from __future__ import annotations

__version__ = "0.1.0"

def test_no_skills_is_warning(self) -> None:
    data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0", "description": "desc"}
    report = validate_agent_card(data)
    assert any(i.severity == "warning" and i.field == "skills" for i in report.issues)
