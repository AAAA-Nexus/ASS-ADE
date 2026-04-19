# Extracted from C:/!ass-ade/tests/test_plan.py:45
# Component id: at.source.ass_ade.test_adding_resets_validated
from __future__ import annotations

__version__ = "0.1.0"

def test_adding_resets_validated(self):
    plan = EditPlan()
    plan.validated = True
    plan.add_create("x.py", "x")
    assert plan.validated is False
