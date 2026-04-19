# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testtrustgate.py:25
# Component id: og.source.ass_ade.test_deny_on_low_trust
__version__ = "0.1.0"

    def test_deny_on_low_trust(self) -> None:
        client = _mock_client()
        client.trust_score.return_value = TrustScore(score=0.3, tier="untrusted")
        result = trust_gate(client, "agent-low-trust")
        assert result.verdict == "DENY"
