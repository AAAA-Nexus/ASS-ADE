# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:7
# Component id: og.source.a3_og_features.testtrustgate
from __future__ import annotations

__version__ = "0.1.0"

class TestTrustGate:
    def test_allow_with_good_scores(self) -> None:
        result = trust_gate(_mock_client(), "agent-1")
        assert result.verdict == "ALLOW"
        assert result.trust_score == 0.85
        assert result.reputation_tier == "gold"
        assert len(result.steps) >= 4

    def test_deny_on_identity_failure(self) -> None:
        client = _mock_client()
        client.identity_verify.return_value = IdentityVerification(decision="deny", actor="test")
        result = trust_gate(client, "agent-bad")
        assert result.verdict == "DENY"

    def test_deny_on_sybil(self) -> None:
        client = _mock_client()
        client.sybil_check.return_value = SybilCheckResult(sybil_risk="high", score=0.9)
        result = trust_gate(client, "agent-sybil")
        assert result.verdict == "DENY"

    def test_deny_on_low_trust(self) -> None:
        client = _mock_client()
        client.trust_score.return_value = TrustScore(score=0.3, tier="untrusted")
        result = trust_gate(client, "agent-low-trust")
        assert result.verdict == "DENY"

    def test_warn_on_medium_trust_without_gold(self) -> None:
        client = _mock_client()
        client.trust_score.return_value = TrustScore(score=0.6, tier="silver")
        client.reputation_score.return_value = ReputationScore(tier="silver", fee_multiplier=1.2)
        result = trust_gate(client, "agent-mid-trust")
        assert result.verdict == "WARN"

    def test_allow_on_medium_trust_with_gold(self) -> None:
        client = _mock_client()
        client.trust_score.return_value = TrustScore(score=0.6, tier="gold")
        client.reputation_score.return_value = ReputationScore(tier="gold", fee_multiplier=1.0)
        result = trust_gate(client, "agent-mid-gold-trust")
        assert result.verdict == "ALLOW"

    def test_validates_agent_id(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            trust_gate(_mock_client(), "")

    def test_exception_handling_identity_sanitized(self) -> None:
        """Exception in identity_verify should not leak raw exception to caller."""
        client = _mock_client()
        client.identity_verify.side_effect = RuntimeError("Connection timeout to server")
        result = trust_gate(client, "agent-error")
        # Verify detail is generic, not raw exception
        identity_step = next(s for s in result.steps if s.name == "identity_verify")
        assert identity_step.detail == "step_failed"
        assert "Connection" not in identity_step.detail
        assert "timeout" not in identity_step.detail
        assert result.verdict == "DENY"

    def test_exception_handling_sybil_sanitized(self) -> None:
        """Exception in sybil_check should not leak raw exception to caller."""
        client = _mock_client()
        client.sybil_check.side_effect = ValueError("Invalid agent signature")
        result = trust_gate(client, "agent-bad-sig")
        sybil_step = next(s for s in result.steps if s.name == "sybil_check")
        assert sybil_step.detail == "step_failed"
        assert "Invalid" not in sybil_step.detail
        assert "signature" not in sybil_step.detail

    def test_exception_handling_trust_sanitized(self) -> None:
        """Exception in trust_score should not leak raw exception to caller."""
        client = _mock_client()
        client.trust_score.side_effect = OSError("Network unreachable")
        result = trust_gate(client, "agent-net-fail")
        trust_step = next(s for s in result.steps if s.name == "trust_score")
        assert trust_step.detail == "step_failed"
        assert "Network" not in trust_step.detail
        assert "unreachable" not in trust_step.detail

    def test_exception_handling_reputation_sanitized(self) -> None:
        """Exception in reputation_score should not leak raw exception to caller."""
        client = _mock_client()
        client.reputation_score.side_effect = NexusServerError("Internal server error: 500")
        result = trust_gate(client, "agent-server-err")
        rep_step = next(s for s in result.steps if s.name == "reputation_score")
        assert rep_step.detail == "step_failed"
        assert "Internal" not in rep_step.detail
        assert "500" not in rep_step.detail
