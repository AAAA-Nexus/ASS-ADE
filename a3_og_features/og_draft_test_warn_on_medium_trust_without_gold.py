# Extracted from C:/!ass-ade/tests/test_workflows.py:88
# Component id: og.source.ass_ade.test_warn_on_medium_trust_without_gold
from __future__ import annotations

__version__ = "0.1.0"

def test_warn_on_medium_trust_without_gold(self) -> None:
    client = _mock_client()
    client.trust_score.return_value = TrustScore(score=0.6, tier="silver")
    client.reputation_score.return_value = ReputationScore(tier="silver", fee_multiplier=1.2)
    result = trust_gate(client, "agent-mid-trust")
    assert result.verdict == "WARN"
