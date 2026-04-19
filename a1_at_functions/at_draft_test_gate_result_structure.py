# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_gate_result_structure.py:7
# Component id: at.source.a1_at_functions.test_gate_result_structure
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_result_structure(self):
    gates = QualityGates(_mock_nexus())
    gates.scan_prompt("test")
    result = gates.gate_log[0]
    assert isinstance(result, GateResult)
    assert result.gate == "prompt_scan"
    assert result.passed is True
    assert result.confidence > 0
