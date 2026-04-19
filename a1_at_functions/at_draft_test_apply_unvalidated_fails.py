# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_apply_unvalidated_fails.py:7
# Component id: at.source.a1_at_functions.test_apply_unvalidated_fails
from __future__ import annotations

__version__ = "0.1.0"

def test_apply_unvalidated_fails(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_create("x.py", "x")
    result = executor.apply(plan)
    assert not result.success
    assert "validated" in result.error.lower()
