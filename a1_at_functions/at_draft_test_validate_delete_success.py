# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_validate_delete_success.py:7
# Component id: at.source.a1_at_functions.test_validate_delete_success
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_delete_success(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_delete("main.py")
    errors = executor.validate(plan)
    assert errors == []
