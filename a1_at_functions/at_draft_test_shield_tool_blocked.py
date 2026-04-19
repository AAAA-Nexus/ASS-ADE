# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_shield_tool_blocked.py:7
# Component id: at.source.a1_at_functions.test_shield_tool_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_shield_tool_blocked(self):
    gates = QualityGates(_mock_nexus(shield_blocked=True))
    result = gates.shield_tool("run_command", {"command": "rm -rf /"})
    assert result is not None
    assert result["blocked"] is True
