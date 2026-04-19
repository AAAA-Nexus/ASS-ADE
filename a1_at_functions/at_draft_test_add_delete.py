# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditplan.py:18
# Component id: at.source.ass_ade.test_add_delete
__version__ = "0.1.0"

    def test_add_delete(self):
        plan = EditPlan()
        plan.add_delete("old.py")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.DELETE
