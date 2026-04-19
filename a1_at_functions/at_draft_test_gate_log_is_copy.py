# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_gate_log_is_copy.py:7
# Component id: at.source.a1_at_functions.test_gate_log_is_copy
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_log_is_copy(self):
    gates = QualityGates(_mock_nexus())
    gates.scan_prompt("test")
    log = gates.gate_log
    log.clear()
    assert len(gates.gate_log) == 1  # original unchanged
