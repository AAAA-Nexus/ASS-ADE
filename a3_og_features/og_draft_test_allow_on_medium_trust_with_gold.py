# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:40
# Component id: og.source.a3_og_features.test_allow_on_medium_trust_with_gold
from __future__ import annotations

__version__ = "0.1.0"

def test_allow_on_medium_trust_with_gold(self) -> None:
    client = _mock_client()
    client.trust_score.return_value = TrustScore(score=0.6, tier="gold")
    client.reputation_score.return_value = ReputationScore(tier="gold", fee_multiplier=1.0)
    result = trust_gate(client, "agent-mid-gold-trust")
    assert result.verdict == "ALLOW"
