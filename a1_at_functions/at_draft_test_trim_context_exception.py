# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trim_context_exception.py:7
# Component id: at.source.a1_at_functions.test_trim_context_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_trim_context_exception(self):
    client = MagicMock()
    client.memory_trim.side_effect = Exception("fail")
    gates = QualityGates(client)
    assert gates.trim_context("text", 100) is None
