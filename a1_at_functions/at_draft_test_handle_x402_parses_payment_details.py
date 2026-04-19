# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_handle_x402_parses_payment_details.py:7
# Component id: at.source.a1_at_functions.test_handle_x402_parses_payment_details
from __future__ import annotations

__version__ = "0.1.0"

def test_handle_x402_parses_payment_details(self) -> None:
    """handle_x402 should extract amount, network, treasury from 402 body."""
    client = self._make_client()
    mock_response = httpx.Response(
        402,
        json={
            "amount": 0.008,
            "network": "base",
            "address": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
            "endpoint": "/v1/trust/score",
            "detail": "Payment required: $0.008 USDC",
        },
    )
    result = client.handle_x402(mock_response)
    assert result["payment_required"] is True
    assert result["amount_usdc"] == 0.008
    assert result["network"] == "base"
    assert result["treasury"] == "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9"
    assert result["endpoint"] == "/v1/trust/score"
    client.close()
