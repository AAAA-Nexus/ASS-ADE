# Extracted from C:/!ass-ade/tests/test_gates.py:108
# Component id: at.source.ass_ade.test_trim_context
from __future__ import annotations

__version__ = "0.1.0"

def test_trim_context(self):
    gates = QualityGates(_mock_nexus(trimmed_context="short version"))
    result = gates.trim_context("very long context...", target_tokens=100)
    assert result == "short version"
