# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_distill_principles_from_failures.py:7
# Component id: at.source.a1_at_functions.test_distill_principles_from_failures
from __future__ import annotations

__version__ = "0.1.0"

def test_distill_principles_from_failures(self) -> None:
    w = WisdomEngine({})
    report = w.run_audit({})  # all failed
    principles = w.distill_principles(report)
    assert isinstance(principles, list)
    assert len(principles) >= 1
    assert all(isinstance(p, str) and p for p in principles)
