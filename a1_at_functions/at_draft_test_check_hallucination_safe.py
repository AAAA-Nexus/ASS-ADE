# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_check_hallucination_safe.py:7
# Component id: at.source.a1_at_functions.test_check_hallucination_safe
from __future__ import annotations

__version__ = "0.1.0"

def test_check_hallucination_safe(self):
    gates = QualityGates(_mock_nexus())
    result = gates.check_hallucination("Python is a programming language.")
    assert result is not None
    assert result["verdict"] == "safe"
    assert "policy_epsilon" in result
