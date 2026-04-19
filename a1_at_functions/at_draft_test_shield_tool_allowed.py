# Extracted from C:/!ass-ade/tests/test_gates.py:83
# Component id: at.source.ass_ade.test_shield_tool_allowed
from __future__ import annotations

__version__ = "0.1.0"

def test_shield_tool_allowed(self):
    gates = QualityGates(_mock_nexus())
    result = gates.shield_tool("read_file", {"path": "test.py"})
    assert result is not None
    assert result["blocked"] is False
