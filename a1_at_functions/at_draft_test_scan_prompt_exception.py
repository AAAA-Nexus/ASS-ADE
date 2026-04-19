# Extracted from C:/!ass-ade/tests/test_gates.py:64
# Component id: at.source.ass_ade.test_scan_prompt_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_prompt_exception(self):
    client = MagicMock()
    client.prompt_inject_scan.side_effect = Exception("network error")
    gates = QualityGates(client)
    assert gates.scan_prompt("test") is None
