# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_plan.py:133
# Component id: at.source.ass_ade.test_apply_multi_file
__version__ = "0.1.0"

    def test_apply_multi_file(self, executor: EditPlanExecutor, workspace: Path):
        plan = EditPlan(description="Multi-file edit")
        plan.add_modify("main.py", "pass", "print('main')")
        plan.add_modify("utils.py", "return 42", "return 99")
        plan.add_create("new.py", "# new file\n")
        executor.validate(plan)
        result = executor.apply(plan)
        assert result.success
        assert "print('main')" in (workspace / "main.py").read_text(encoding="utf-8")
        assert "return 99" in (workspace / "utils.py").read_text(encoding="utf-8")
        assert (workspace / "new.py").exists()
