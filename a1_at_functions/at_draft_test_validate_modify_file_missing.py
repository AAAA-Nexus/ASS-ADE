# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditplanexecutor.py:35
# Component id: at.source.ass_ade.test_validate_modify_file_missing
__version__ = "0.1.0"

    def test_validate_modify_file_missing(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_modify("ghost.py", "old", "new")
        errors = executor.validate(plan)
        assert len(errors) == 1
