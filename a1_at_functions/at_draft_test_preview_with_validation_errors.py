# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditplanexecutor.py:104
# Component id: at.source.ass_ade.test_preview_with_validation_errors
__version__ = "0.1.0"

    def test_preview_with_validation_errors(self, executor: EditPlanExecutor):
        plan = EditPlan()
        plan.add_modify("ghost.py", "old", "new")
        preview = executor.preview(plan)
        assert "error" in preview.lower() or "Validation" in preview
