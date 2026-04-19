# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_validate_modify_success.py:7
# Component id: at.source.a1_at_functions.test_validate_modify_success
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_modify_success(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_modify("main.py", "pass", "print('hello')")
    errors = executor.validate(plan)
    assert errors == []
    assert plan.validated is True
    assert plan.edits[0].diff  # diff populated
