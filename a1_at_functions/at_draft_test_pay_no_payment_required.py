# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:419
# Component id: at.source.ass_ade.test_pay_no_payment_required
__version__ = "0.1.0"

    def test_pay_no_payment_required(self, tmp_path: Path) -> None:
        """If endpoint returns 200, pay should show results without payment."""
        mock_nx = MagicMock()
        mock_nx._post_with_x402.return_value = {"trust_score": 0.95}
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pay", "/v1/trust/score", "--config", str(_hybrid_config(tmp_path))],
            )
        assert result.exit_code == 0
        assert "No payment required" in result.stdout
