# Extracted from C:/!ass-ade/tests/test_plan.py:88
# Component id: at.source.ass_ade.test_validate_delete_success
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_delete_success(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_delete("main.py")
    errors = executor.validate(plan)
    assert errors == []
