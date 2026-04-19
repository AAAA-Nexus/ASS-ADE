# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_plan.py:109
# Component id: at.source.ass_ade.test_apply_modify
__version__ = "0.1.0"

    def test_apply_modify(self, executor: EditPlanExecutor, workspace: Path):
        plan = EditPlan()
        plan.add_modify("main.py", "pass", "print('hello')")
        executor.validate(plan)
        result = executor.apply(plan)
        assert result.success
        content = (workspace / "main.py").read_text(encoding="utf-8")
        assert "print('hello')" in content
