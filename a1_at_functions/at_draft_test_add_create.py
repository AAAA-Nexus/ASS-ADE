# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_plan.py:27
# Component id: at.source.ass_ade.test_add_create
__version__ = "0.1.0"

    def test_add_create(self):
        plan = EditPlan(description="Test plan")
        plan.add_create("new.py", "print('new')\n")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.CREATE
