# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_certify_passed.py:7
# Component id: at.source.a1_at_functions.test_certify_passed
from __future__ import annotations

__version__ = "0.1.0"

def test_certify_passed(self):
    gates = QualityGates(_mock_nexus())
    result = gates.certify("def add(a, b): return a + b")
    assert result is not None
    assert result["passed"] is True
    assert result["certificate_id"] == "cert-123"
