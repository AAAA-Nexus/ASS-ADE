# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testtrustgate.py:6
# Component id: og.source.ass_ade.test_allow_with_good_scores
__version__ = "0.1.0"

    def test_allow_with_good_scores(self) -> None:
        result = trust_gate(_mock_client(), "agent-1")
        assert result.verdict == "ALLOW"
        assert result.trust_score == 0.85
        assert result.reputation_tier == "gold"
        assert len(result.steps) >= 4
