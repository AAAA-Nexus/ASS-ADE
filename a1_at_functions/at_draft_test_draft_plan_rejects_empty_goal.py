# Extracted from C:/!ass-ade/tests/test_planner.py:13
# Component id: at.source.ass_ade.test_draft_plan_rejects_empty_goal
from __future__ import annotations

__version__ = "0.1.0"

def test_draft_plan_rejects_empty_goal() -> None:
    with pytest.raises(ValueError):
        draft_plan("   ")
