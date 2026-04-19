# Extracted from C:/!ass-ade/tests/test_workflows.py:82
# Component id: og.source.ass_ade.test_deny_on_low_trust
from __future__ import annotations

__version__ = "0.1.0"

def test_deny_on_low_trust(self) -> None:
    client = _mock_client()
    client.trust_score.return_value = TrustScore(score=0.3, tier="untrusted")
    result = trust_gate(client, "agent-low-trust")
    assert result.verdict == "DENY"
