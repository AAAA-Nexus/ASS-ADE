# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_apply_create.py:7
# Component id: at.source.a1_at_functions.test_apply_create
from __future__ import annotations

__version__ = "0.1.0"

def test_apply_create(self, executor: EditPlanExecutor, workspace: Path):
    plan = EditPlan()
    plan.add_create("created.py", "print('created')\n")
    executor.validate(plan)
    result = executor.apply(plan)
    assert result.success
    assert (workspace / "created.py").read_text(encoding="utf-8") == "print('created')\n"
    assert plan.applied is True
