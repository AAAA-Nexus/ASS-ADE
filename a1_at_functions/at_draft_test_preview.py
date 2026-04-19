# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_preview.py:7
# Component id: at.source.a1_at_functions.test_preview
from __future__ import annotations

__version__ = "0.1.0"

def test_preview(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_modify("main.py", "pass", "print('hello')")
    preview = executor.preview(plan)
    assert "pass" in preview or "print" in preview
