# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_fail_open_on_exception.py:7
# Component id: at.source.a1_at_functions.test_fail_open_on_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_fail_open_on_exception(self):
    client = MagicMock()
    client.prompt_inject_scan.side_effect = Exception("network error")
    client.hallucination_oracle.side_effect = Exception("network error")
    client.security_shield.side_effect = Exception("network error")
    client.certify_output.side_effect = Exception("network error")
    gates = QualityGates(client)

    assert gates.scan_prompt("test") is None
    assert gates.check_hallucination("test") is None
    assert gates.shield_tool("x", {}) is None
    assert gates.certify("test") is None
