# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_adding_resets_validated.py:7
# Component id: at.source.a1_at_functions.test_adding_resets_validated
from __future__ import annotations

__version__ = "0.1.0"

def test_adding_resets_validated(self):
    plan = EditPlan()
    plan.validated = True
    plan.add_create("x.py", "x")
    assert plan.validated is False
