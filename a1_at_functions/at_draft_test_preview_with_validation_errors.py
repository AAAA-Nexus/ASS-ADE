# Extracted from C:/!ass-ade/tests/test_plan.py:151
# Component id: at.source.ass_ade.test_preview_with_validation_errors
from __future__ import annotations

__version__ = "0.1.0"

def test_preview_with_validation_errors(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_modify("ghost.py", "old", "new")
    preview = executor.preview(plan)
    assert "error" in preview.lower() or "Validation" in preview
