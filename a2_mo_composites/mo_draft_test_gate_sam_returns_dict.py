# Extracted from C:/!ass-ade/tests/test_phase_engines.py:164
# Component id: mo.source.ass_ade.test_gate_sam_returns_dict
from __future__ import annotations

__version__ = "0.1.0"

def test_gate_sam_returns_dict(self):
    gates = self._make_gates()
    result = gates.gate_sam(target="test_target")
    assert result is not None
    assert "trs" in result
    assert "g23" in result
    assert "composite" in result
    assert "passed" in result
