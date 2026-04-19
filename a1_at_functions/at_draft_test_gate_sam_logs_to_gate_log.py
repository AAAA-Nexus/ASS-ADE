# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_gate_sam_logs_to_gate_log.py:7
# Component id: at.source.a1_at_functions.test_gate_sam_logs_to_gate_log
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_sam_logs_to_gate_log(self):
    gates = self._make_gates()
    gates.gate_sam(target="x")
    assert any(g.gate == "sam" for g in gates.gate_log)
