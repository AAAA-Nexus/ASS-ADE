# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_prompt_clean.py:7
# Component id: at.source.a1_at_functions.test_scan_prompt_clean
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_prompt_clean(self):
    gates = QualityGates(_mock_nexus())
    result = gates.scan_prompt("What is Python?")
    assert result is not None
    assert result["blocked"] is False
