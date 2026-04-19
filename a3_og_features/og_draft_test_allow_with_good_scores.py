# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:8
# Component id: og.source.a3_og_features.test_allow_with_good_scores
from __future__ import annotations

__version__ = "0.1.0"

def test_allow_with_good_scores(self) -> None:
    result = trust_gate(_mock_client(), "agent-1")
    assert result.verdict == "ALLOW"
    assert result.trust_score == 0.85
    assert result.reputation_tier == "gold"
    assert len(result.steps) >= 4
