# Extracted from C:/!ass-ade/tests/test_gates.py:113
# Component id: at.source.ass_ade.test_trim_context_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_trim_context_exception(self):
    client = MagicMock()
    client.memory_trim.side_effect = Exception("fail")
    gates = QualityGates(client)
    assert gates.trim_context("text", 100) is None
