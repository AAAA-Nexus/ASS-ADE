# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_explicit_qn_override.py:7
# Component id: at.source.a1_at_functions.test_explicit_qn_override
from __future__ import annotations

__version__ = "0.1.0"

def test_explicit_qN_override(self) -> None:
    w = WisdomEngine({})
    report = w.run_audit({"q1": True, "q2": False, "q3": True})
    # q1 and q3 explicitly True, q2 False
    assert report.passed >= 2
    found_q2_fail = any(f["id"] == 2 for f in report.failures)
    assert found_q2_fail
