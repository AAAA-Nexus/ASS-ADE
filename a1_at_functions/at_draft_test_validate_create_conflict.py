# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_validate_create_conflict.py:7
# Component id: at.source.a1_at_functions.test_validate_create_conflict
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_create_conflict(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_create("main.py", "conflict")
    errors = executor.validate(plan)
    assert len(errors) == 1
    assert "already exists" in errors[0]
