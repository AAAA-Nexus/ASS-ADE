# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a3_og_features/og_draft_testtrustgate.py:13
# Component id: og.source.ass_ade.test_deny_on_identity_failure
__version__ = "0.1.0"

    def test_deny_on_identity_failure(self) -> None:
        client = _mock_client()
        client.identity_verify.return_value = IdentityVerification(decision="deny", actor="test")
        result = trust_gate(client, "agent-bad")
        assert result.verdict == "DENY"
