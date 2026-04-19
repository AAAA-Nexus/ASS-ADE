# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_plan.py:118
# Component id: at.source.ass_ade.test_apply_delete
__version__ = "0.1.0"

    def test_apply_delete(self, executor: EditPlanExecutor, workspace: Path):
        plan = EditPlan()
        plan.add_delete("utils.py")
        executor.validate(plan)
        result = executor.apply(plan)
        assert result.success
        assert not (workspace / "utils.py").exists()
