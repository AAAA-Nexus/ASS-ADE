# Extracted from C:/!ass-ade/tests/test_plan.py:39
# Component id: at.source.ass_ade.test_add_delete
from __future__ import annotations

__version__ = "0.1.0"

def test_add_delete(self):
    plan = EditPlan()
    plan.add_delete("old.py")
    assert len(plan.edits) == 1
    assert plan.edits[0].kind == EditKind.DELETE
