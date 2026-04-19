# Extracted from C:/!ass-ade/tests/test_gates.py:70
# Component id: at.source.ass_ade.test_check_hallucination_safe
from __future__ import annotations

__version__ = "0.1.0"

def test_check_hallucination_safe(self):
    gates = QualityGates(_mock_nexus())
    result = gates.check_hallucination("Python is a programming language.")
    assert result is not None
    assert result["verdict"] == "safe"
    assert "policy_epsilon" in result
