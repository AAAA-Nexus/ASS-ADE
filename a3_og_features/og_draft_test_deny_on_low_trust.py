# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:27
# Component id: og.source.a3_og_features.test_deny_on_low_trust
from __future__ import annotations

__version__ = "0.1.0"

def test_deny_on_low_trust(self) -> None:
    client = _mock_client()
    client.trust_score.return_value = TrustScore(score=0.3, tier="untrusted")
    result = trust_gate(client, "agent-low-trust")
    assert result.verdict == "DENY"
