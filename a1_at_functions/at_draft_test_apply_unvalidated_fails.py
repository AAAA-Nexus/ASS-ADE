# Extracted from C:/!ass-ade/tests/test_plan.py:126
# Component id: at.source.ass_ade.test_apply_unvalidated_fails
from __future__ import annotations

__version__ = "0.1.0"

def test_apply_unvalidated_fails(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_create("x.py", "x")
    result = executor.apply(plan)
    assert not result.success
    assert "validated" in result.error.lower()
