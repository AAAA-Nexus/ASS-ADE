# Extracted from C:/!ass-ade/tests/test_plan.py:94
# Component id: at.source.ass_ade.test_validate_delete_not_found
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_delete_not_found(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_delete("nonexistent.py")
    errors = executor.validate(plan)
    assert len(errors) == 1
