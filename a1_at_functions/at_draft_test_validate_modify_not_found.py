# Extracted from C:/!ass-ade/tests/test_plan.py:75
# Component id: at.source.ass_ade.test_validate_modify_not_found
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_modify_not_found(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_modify("main.py", "NONEXISTENT", "replacement")
    errors = executor.validate(plan)
    assert len(errors) == 1
    assert "not found" in errors[0]
