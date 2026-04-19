# Extracted from C:/!ass-ade/tests/test_workflows.py:63
# Component id: og.source.ass_ade.test_allow_with_good_scores
from __future__ import annotations

__version__ = "0.1.0"

def test_allow_with_good_scores(self) -> None:
    result = trust_gate(_mock_client(), "agent-1")
    assert result.verdict == "ALLOW"
    assert result.trust_score == 0.85
    assert result.reputation_tier == "gold"
    assert len(result.steps) >= 4
