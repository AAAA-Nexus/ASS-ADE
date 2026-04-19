# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_shield_tool.py:7
# Component id: at.source.a1_at_functions.test_shield_tool
from __future__ import annotations

__version__ = "0.1.0"

def test_shield_tool(self):
    gates = QualityGates(self._mock_client())
    result = gates.shield_tool("read_file", {"path": "main.py"})
    assert result is not None
    assert not result["blocked"]
