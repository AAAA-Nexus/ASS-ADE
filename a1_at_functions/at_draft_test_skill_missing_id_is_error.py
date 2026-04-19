# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_skill_missing_id_is_error.py:7
# Component id: at.source.a1_at_functions.test_skill_missing_id_is_error
from __future__ import annotations

__version__ = "0.1.0"

def test_skill_missing_id_is_error(self) -> None:
    data = {
        "name": "TestAgent",
        "url": "https://example.com",
        "version": "1.0",
        "skills": [{"id": "", "name": "Skill One"}],
    }
    report = validate_agent_card(data)
    assert not report.valid
