# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditplanexecutor.py:41
# Component id: at.source.ass_ade.test_validate_delete_success
__version__ = "0.1.0"

    def test_validate_delete_success(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_delete("main.py")
        errors = executor.validate(plan)
        assert errors == []
