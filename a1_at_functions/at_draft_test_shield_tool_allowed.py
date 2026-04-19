# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_shield_tool_allowed.py:7
# Component id: at.source.a1_at_functions.test_shield_tool_allowed
from __future__ import annotations

__version__ = "0.1.0"

def test_shield_tool_allowed(self):
    gates = QualityGates(_mock_nexus())
    result = gates.shield_tool("read_file", {"path": "test.py"})
    assert result is not None
    assert result["blocked"] is False
