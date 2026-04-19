# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testworkflowtrustgate.py:7
# Component id: og.source.a3_og_features.testworkflowtrustgate
from __future__ import annotations

__version__ = "0.1.0"

class TestWorkflowTrustGate:
    """Test `workflow trust-gate` command — multi-step agent trust gating."""

    def test_workflow_trust_gate_allow(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Trust gate should return ALLOW verdict for trusted agent."""
        mock_nx = MagicMock()
        mock_nx.trust_score.return_value = TrustScore(
            agent_id="agent-trusted",
            score=0.95,
            tier="platinum",
            certified_monotonic=True,
        )
        mock_nx.reputation_score.return_value = {
            "agent_id": "agent-trusted",
            "tier": "gold",
            "score": 0.90,
        }

        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["workflow", "trust-gate", "agent-trusted", "--config", str(hybrid_config)],
            )

        assert result.exit_code == 0
