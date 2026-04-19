# Extracted from C:/!ass-ade/tests/test_agent.py:100
# Component id: at.source.ass_ade.test_scan_prompt_safe
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_prompt_safe(self):
    gates = QualityGates(self._mock_client())
    result = gates.scan_prompt("hello world")
    assert result is not None
    assert not result["blocked"]
