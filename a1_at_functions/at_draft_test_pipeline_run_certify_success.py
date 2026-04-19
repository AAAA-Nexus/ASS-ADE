# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:404
# Component id: at.source.ass_ade.test_pipeline_run_certify_success
__version__ = "0.1.0"

    def test_pipeline_run_certify_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Certify pipeline should verify hallucination, ethics, compliance, and certify output."""
        mock_nx = MagicMock()
        
        # Mock the four certify steps
        hallucination_result = MagicMock()
        hallucination_result.model_dump.return_value = {"verdict": "safe"}
        mock_nx.hallucination_oracle.return_value = hallucination_result
        
        ethics_result = MagicMock()
        ethics_result.model_dump.return_value = {"safe": True}
        mock_nx.ethics_check.return_value = ethics_result
        
        compliance_result = MagicMock()
        compliance_result.model_dump.return_value = {"compliant": True}
        mock_nx.compliance_check.return_value = compliance_result
        
        certify_result = MagicMock()
        certify_result.model_dump.return_value = {"certificate_id": "cert-2025-12345"}
        mock_nx.certify_output.return_value = certify_result
        
        test_text = "The Earth is round and orbits the Sun."
        
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pipeline", "run", "certify", test_text, "--config", str(hybrid_config), "--no-persist"],
            )
        
        assert result.exit_code == 0, f"Pipeline failed:\n{result.stdout}"
        assert "Running pipeline" in result.stdout
        assert "certify-output" in result.stdout or "certify" in result.stdout.lower()
        # Verify all certify steps were called
        assert mock_nx.hallucination_oracle.called
        assert mock_nx.ethics_check.called
        assert mock_nx.compliance_check.called
        assert mock_nx.certify_output.called
