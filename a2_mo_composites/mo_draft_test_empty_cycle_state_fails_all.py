# Extracted from C:/!ass-ade/tests/test_engine_integration.py:57
# Component id: mo.source.ass_ade.test_empty_cycle_state_fails_all
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_cycle_state_fails_all(self) -> None:
    w = WisdomEngine({})
    report = w.run_audit({})
    assert report.failed == 50
    assert report.passed == 0
    assert report.score == 0.0
