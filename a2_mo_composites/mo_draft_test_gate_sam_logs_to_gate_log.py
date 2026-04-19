# Extracted from C:/!ass-ade/tests/test_phase_engines.py:173
# Component id: mo.source.ass_ade.test_gate_sam_logs_to_gate_log
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_sam_logs_to_gate_log(self):
    gates = self._make_gates()
    gates.gate_sam(target="x")
    assert any(g.gate == "sam" for g in gates.gate_log)
