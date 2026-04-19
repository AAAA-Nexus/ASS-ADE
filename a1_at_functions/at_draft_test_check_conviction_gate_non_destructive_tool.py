# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_check_conviction_gate_non_destructive_tool.py:7
# Component id: at.source.a1_at_functions.test_check_conviction_gate_non_destructive_tool
from __future__ import annotations

__version__ = "0.1.0"

def test_check_conviction_gate_non_destructive_tool(self):
    orch = self._make()
    # Non-destructive tool: read_file should NOT be blocked
    blocked = orch.check_conviction_gate("read_file", {})
    assert blocked is False
