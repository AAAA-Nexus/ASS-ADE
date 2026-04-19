# Extracted from C:/!ass-ade/tests/test_workflows.py:76
# Component id: og.source.ass_ade.test_deny_on_sybil
from __future__ import annotations

__version__ = "0.1.0"

def test_deny_on_sybil(self) -> None:
    client = _mock_client()
    client.sybil_check.return_value = SybilCheckResult(sybil_risk="high", score=0.9)
    result = trust_gate(client, "agent-sybil")
    assert result.verdict == "DENY"
