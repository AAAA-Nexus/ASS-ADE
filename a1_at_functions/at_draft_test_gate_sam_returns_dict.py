# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_gate_sam_returns_dict.py:7
# Component id: at.source.a1_at_functions.test_gate_sam_returns_dict
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
