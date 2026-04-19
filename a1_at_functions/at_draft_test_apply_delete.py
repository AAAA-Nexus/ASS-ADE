# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_apply_delete.py:7
# Component id: at.source.a1_at_functions.test_apply_delete
from __future__ import annotations

__version__ = "0.1.0"

def test_apply_delete(self, executor: EditPlanExecutor, workspace: Path):
    plan = EditPlan()
    plan.add_delete("utils.py")
    executor.validate(plan)
    result = executor.apply(plan)
    assert result.success
    assert not (workspace / "utils.py").exists()
