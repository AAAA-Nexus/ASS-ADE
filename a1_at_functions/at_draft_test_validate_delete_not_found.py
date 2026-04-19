# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditplanexecutor.py:47
# Component id: at.source.ass_ade.test_validate_delete_not_found
__version__ = "0.1.0"

    def test_validate_delete_not_found(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_delete("nonexistent.py")
        errors = executor.validate(plan)
        assert len(errors) == 1
