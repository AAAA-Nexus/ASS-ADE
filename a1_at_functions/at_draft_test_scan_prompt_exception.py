# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_prompt_exception.py:7
# Component id: at.source.a1_at_functions.test_scan_prompt_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_prompt_exception(self):
    client = MagicMock()
    client.prompt_inject_scan.side_effect = Exception("network error")
    gates = QualityGates(client)
    assert gates.scan_prompt("test") is None
