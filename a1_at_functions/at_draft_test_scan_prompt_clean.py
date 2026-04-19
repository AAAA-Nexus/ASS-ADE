# Extracted from C:/!ass-ade/tests/test_gates.py:51
# Component id: at.source.ass_ade.test_scan_prompt_clean
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_prompt_clean(self):
    gates = QualityGates(_mock_nexus())
    result = gates.scan_prompt("What is Python?")
    assert result is not None
    assert result["blocked"] is False
