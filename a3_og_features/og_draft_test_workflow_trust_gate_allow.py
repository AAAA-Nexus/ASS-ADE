# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:578
# Component id: og.source.ass_ade.test_workflow_trust_gate_allow
__version__ = "0.1.0"

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
