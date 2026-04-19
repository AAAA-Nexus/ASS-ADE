# Extracted from C:/!ass-ade/tests/test_gates.py:89
# Component id: at.source.ass_ade.test_shield_tool_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_shield_tool_blocked(self):
    gates = QualityGates(_mock_nexus(shield_blocked=True))
    result = gates.shield_tool("run_command", {"command": "rm -rf /"})
    assert result is not None
    assert result["blocked"] is True
