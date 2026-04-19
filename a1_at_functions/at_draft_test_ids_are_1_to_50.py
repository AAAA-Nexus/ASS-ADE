# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testauditquestions.py:15
# Component id: at.source.a2_mo_composites.test_ids_are_1_to_50
from __future__ import annotations

__version__ = "0.1.0"

def test_ids_are_1_to_50(self) -> None:
    ids = sorted(q["id"] for q in AUDIT_QUESTIONS)
    assert ids == list(range(1, 51))
