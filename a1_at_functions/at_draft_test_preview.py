# Extracted from C:/!ass-ade/tests/test_plan.py:145
# Component id: at.source.ass_ade.test_preview
from __future__ import annotations

__version__ = "0.1.0"

def test_preview(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_modify("main.py", "pass", "print('hello')")
    preview = executor.preview(plan)
    assert "pass" in preview or "print" in preview
