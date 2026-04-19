# Extracted from C:/!ass-ade/tests/test_plan.py:53
# Component id: at.source.ass_ade.test_validate_create_success
from __future__ import annotations

__version__ = "0.1.0"

def test_validate_create_success(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_create("brand_new.py", "content")
    errors = executor.validate(plan)
    assert errors == []
    assert plan.validated is True
