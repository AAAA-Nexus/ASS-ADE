# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_validate_delete_not_found.py:7
# Component id: at.source.a1_at_functions.test_validate_delete_not_found
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_delete_not_found(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_delete("nonexistent.py")
    errors = executor.validate(plan)
    assert len(errors) == 1
