# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditplan.py:24
# Component id: at.source.ass_ade.test_adding_resets_validated
__version__ = "0.1.0"

    def test_adding_resets_validated(self):
        plan = EditPlan()
        plan.validated = True
        plan.add_create("x.py", "x")
        assert plan.validated is False
