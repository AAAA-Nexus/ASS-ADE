# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:335
# Component id: at.source.ass_ade.test_pipeline_run_trust_gate_success
__version__ = "0.1.0"

    def test_pipeline_run_trust_gate_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Trust-gate pipeline should verify identity, sybil, trust, and reputation."""
        mock_nx = MagicMock()
        
        # Mock the four trust-gate steps
        identity_result = MagicMock()
        identity_result.model_dump.return_value = {"decision": "allow"}
        mock_nx.identity_verify.return_value = identity_result
        
        sybil_result = MagicMock()
        sybil_result.model_dump.return_value = {"sybil_risk": "low"}
        mock_nx.sybil_check.return_value = sybil_result
        
        trust_result = MagicMock()
        trust_result.model_dump.return_value = {"score": 0.85}
        mock_nx.trust_score.return_value = trust_result
        
        reputation_result = MagicMock()
        reputation_result.model_dump.return_value = {"tier": "gold"}
        mock_nx.reputation_score.return_value = reputation_result
        
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pipeline", "run", "trust-gate", "agent-test-001", "--config", str(hybrid_config), "--no-persist"],
            )
        
        assert result.exit_code == 0, f"Pipeline failed:\n{result.stdout}"
        # Verify pipeline ran and produced output
        assert "Running pipeline" in result.stdout
        assert "identity_verify" in result.stdout or "identity" in result.stdout.lower()
        assert "gate_decision" in result.stdout or "gate" in result.stdout.lower()
        # Verify all trust-gate steps were mentioned
        assert mock_nx.identity_verify.called
        assert mock_nx.sybil_check.called
        assert mock_nx.trust_score.called
        assert mock_nx.reputation_score.called
