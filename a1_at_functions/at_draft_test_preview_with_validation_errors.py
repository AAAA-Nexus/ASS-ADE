# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_preview_with_validation_errors.py:7
# Component id: at.source.a1_at_functions.test_preview_with_validation_errors
from __future__ import annotations

__version__ = "0.1.0"

def test_preview_with_validation_errors(self, executor: EditPlanExecutor):
    plan = EditPlan()
    plan.add_modify("ghost.py", "old", "new")
    preview = executor.preview(plan)
    assert "error" in preview.lower() or "Validation" in preview
