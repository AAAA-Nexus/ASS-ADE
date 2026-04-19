# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:418
# Component id: mo.source.ass_ade.testpaycommand
__version__ = "0.1.0"

class TestPayCommand:
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

    def test_pay_shows_challenge(self, tmp_path: Path) -> None:
        """If endpoint returns 402, pay should show the payment challenge."""
        mock_nx = MagicMock()
        challenge = PaymentChallenge.from_response({
            "amount_micro_usdc": 8000,
            "amount_usdc": "0.008000",
            "recipient": ATOMADIC_TREASURY,
            "endpoint": "/v1/trust/score",
            "chain_id": 84532,
        })
        mock_nx._post_with_x402.return_value = {
            "payment_required": True,
            "challenge": challenge,  # New: typed challenge in response
            "raw": {
                "amount_micro_usdc": 8000,
                "amount_usdc": "0.008000",
                "recipient": ATOMADIC_TREASURY,
                "endpoint": "/v1/trust/score",
                "chain_id": 84532,
            },
        }
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pay", "/v1/trust/score", "--config", str(_hybrid_config(tmp_path))],
                input="n\n",  # Decline payment
            )
        assert "Payment Required" in result.stdout or "0.008000" in result.stdout
