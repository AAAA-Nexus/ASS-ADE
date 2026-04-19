# Extracted from C:/!ass-ade/tests/test_gates.py:121
# Component id: at.source.ass_ade.test_gate_log_accumulates
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_log_accumulates(self):
    gates = QualityGates(_mock_nexus())
    gates.scan_prompt("test")
    gates.check_hallucination("output")
    gates.certify("code")
    assert len(gates.gate_log) == 3
