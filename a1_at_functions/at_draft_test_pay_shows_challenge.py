# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_pay_shows_challenge.py:7
# Component id: at.source.a1_at_functions.test_pay_shows_challenge
from __future__ import annotations

__version__ = "0.1.0"

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
