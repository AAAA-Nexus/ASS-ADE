# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testeditplan.py:7
# Component id: mo.source.a2_mo_composites.testeditplan
from __future__ import annotations

__version__ = "0.1.0"

class TestEditPlan:
    def test_add_create(self):
        plan = EditPlan(description="Test plan")
        plan.add_create("new.py", "print('new')\n")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.CREATE

    def test_add_modify(self):
        plan = EditPlan()
        plan.add_modify("main.py", "pass", "print('hello')")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.MODIFY

    def test_add_delete(self):
        plan = EditPlan()
        plan.add_delete("old.py")
        assert len(plan.edits) == 1
        assert plan.edits[0].kind == EditKind.DELETE

    def test_adding_resets_validated(self):
        plan = EditPlan()
        plan.validated = True
        plan.add_create("x.py", "x")
        assert plan.validated is False
