# Extracted from C:/!ass-ade/tests/test_phase_engines.py:658
# Component id: mo.source.ass_ade.test_check_conviction_gate_non_destructive_tool
from __future__ import annotations

__version__ = "0.1.0"

def test_check_conviction_gate_non_destructive_tool(self):
    orch = self._make()
    # Non-destructive tool: read_file should NOT be blocked
    blocked = orch.check_conviction_gate("read_file", {})
    assert blocked is False
