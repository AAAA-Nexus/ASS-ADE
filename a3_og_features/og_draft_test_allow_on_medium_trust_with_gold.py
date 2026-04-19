# Extracted from C:/!ass-ade/tests/test_workflows.py:95
# Component id: og.source.ass_ade.test_allow_on_medium_trust_with_gold
from __future__ import annotations

__version__ = "0.1.0"

def test_allow_on_medium_trust_with_gold(self) -> None:
    client = _mock_client()
    client.trust_score.return_value = TrustScore(score=0.6, tier="gold")
    client.reputation_score.return_value = ReputationScore(tier="gold", fee_multiplier=1.0)
    result = trust_gate(client, "agent-mid-gold-trust")
    assert result.verdict == "ALLOW"
