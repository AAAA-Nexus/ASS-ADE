# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_apply_modify.py:7
# Component id: at.source.a1_at_functions.test_apply_modify
from __future__ import annotations

__version__ = "0.1.0"

def test_apply_modify(self, executor: EditPlanExecutor, workspace: Path):
    plan = EditPlan()
    plan.add_modify("main.py", "pass", "print('hello')")
    executor.validate(plan)
    result = executor.apply(plan)
    assert result.success
    content = (workspace / "main.py").read_text(encoding="utf-8")
    assert "print('hello')" in content
