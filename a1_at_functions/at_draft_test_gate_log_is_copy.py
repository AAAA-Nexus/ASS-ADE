# Extracted from C:/!ass-ade/tests/test_gates.py:128
# Component id: at.source.ass_ade.test_gate_log_is_copy
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_log_is_copy(self):
    gates = QualityGates(_mock_nexus())
    gates.scan_prompt("test")
    log = gates.gate_log
    log.clear()
    assert len(gates.gate_log) == 1  # original unchanged
