# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testtrustgate.py:19
# Component id: og.source.ass_ade.test_deny_on_sybil
__version__ = "0.1.0"

    def test_deny_on_sybil(self) -> None:
        client = _mock_client()
        client.sybil_check.return_value = SybilCheckResult(sybil_risk="high", score=0.9)
        result = trust_gate(client, "agent-sybil")
        assert result.verdict == "DENY"
