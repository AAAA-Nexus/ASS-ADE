# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_draft_plan_rejects_empty_goal.py:7
# Component id: at.source.a1_at_functions.test_draft_plan_rejects_empty_goal
from __future__ import annotations

__version__ = "0.1.0"

def test_draft_plan_rejects_empty_goal() -> None:
    with pytest.raises(ValueError):
        draft_plan("   ")
