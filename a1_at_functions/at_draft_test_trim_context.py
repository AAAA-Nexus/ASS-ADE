# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trim_context.py:7
# Component id: at.source.a1_at_functions.test_trim_context
from __future__ import annotations

__version__ = "0.1.0"

def test_trim_context(self):
    gates = QualityGates(_mock_nexus(trimmed_context="short version"))
    result = gates.trim_context("very long context...", target_tokens=100)
    assert result == "short version"
