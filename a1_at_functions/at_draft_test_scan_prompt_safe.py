# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_prompt_safe.py:7
# Component id: at.source.a1_at_functions.test_scan_prompt_safe
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_prompt_safe(self):
    gates = QualityGates(self._mock_client())
    result = gates.scan_prompt("hello world")
    assert result is not None
    assert not result["blocked"]
