# Extracted from C:/!ass-ade/tests/test_plan.py:67
# Component id: at.source.ass_ade.test_validate_modify_success
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_modify_success(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_modify("main.py", "pass", "print('hello')")
    errors = executor.validate(plan)
    assert errors == []
    assert plan.validated is True
    assert plan.edits[0].diff  # diff populated
