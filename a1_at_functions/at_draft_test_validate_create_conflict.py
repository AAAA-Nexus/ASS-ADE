# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditplanexecutor.py:13
# Component id: at.source.ass_ade.test_validate_create_conflict
__version__ = "0.1.0"

    def test_validate_create_conflict(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_create("main.py", "conflict")
        errors = executor.validate(plan)
        assert len(errors) == 1
        assert "already exists" in errors[0]
