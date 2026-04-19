# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_certify_failed.py:7
# Component id: at.source.a1_at_functions.test_certify_failed
from __future__ import annotations

__version__ = "0.1.0"

def test_certify_failed(self):
    gates = QualityGates(_mock_nexus(rubric_passed=False, cert_score=0.3))
    result = gates.certify("bad code")
    assert result is not None
    assert result["passed"] is False
