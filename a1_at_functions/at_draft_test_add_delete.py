# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_add_delete.py:7
# Component id: at.source.a1_at_functions.test_add_delete
from __future__ import annotations

__version__ = "0.1.0"

def test_add_delete(self):
    plan = EditPlan()
    plan.add_delete("old.py")
    assert len(plan.edits) == 1
    assert plan.edits[0].kind == EditKind.DELETE
