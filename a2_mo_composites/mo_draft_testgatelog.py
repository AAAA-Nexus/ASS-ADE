# Extracted from C:/!ass-ade/tests/test_gates.py:120
# Component id: mo.source.ass_ade.testgatelog
from __future__ import annotations

__version__ = "0.1.0"

class TestGateLog:
    def test_gate_log_accumulates(self):
        gates = QualityGates(_mock_nexus())
        gates.scan_prompt("test")
        gates.check_hallucination("output")
        gates.certify("code")
        assert len(gates.gate_log) == 3

    def test_gate_log_is_copy(self):
        gates = QualityGates(_mock_nexus())
        gates.scan_prompt("test")
        log = gates.gate_log
        log.clear()
        assert len(gates.gate_log) == 1  # original unchanged

    def test_gate_result_structure(self):
        gates = QualityGates(_mock_nexus())
        gates.scan_prompt("test")
        result = gates.gate_log[0]
        assert isinstance(result, GateResult)
        assert result.gate == "prompt_scan"
        assert result.passed is True
        assert result.confidence > 0
