# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_check_hallucination_unsafe.py:7
# Component id: at.source.a1_at_functions.test_check_hallucination_unsafe
from __future__ import annotations

__version__ = "0.1.0"

def test_check_hallucination_unsafe(self):
    gates = QualityGates(_mock_nexus(verdict="unsafe", policy_epsilon=0.85))
    result = gates.check_hallucination("Made up claim.")
    assert result is not None
    assert result["verdict"] == "unsafe"
