# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_plan.py:53
# Component id: at.source.ass_ade.test_validate_create_success
__version__ = "0.1.0"

    def test_validate_create_success(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_create("brand_new.py", "content")
        errors = executor.validate(plan)
        assert errors == []
        assert plan.validated is True
