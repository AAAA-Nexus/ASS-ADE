# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_post_with_x402_returns_payment_on_402.py:7
# Component id: at.source.a1_at_functions.test_post_with_x402_returns_payment_on_402
from __future__ import annotations

__version__ = "0.1.0"

def test_post_with_x402_returns_payment_on_402(self) -> None:
    """_post_with_x402 should return payment details instead of raising on 402."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            402,
            json={"amount": 0.008, "network": "base", "address": "0xTREASURY"},
        )

    transport = httpx.MockTransport(handler)
    client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
    result = client._post_with_x402("/v1/trust/score", {"agent_id": "test"})
    assert result["payment_required"] is True
    assert result["amount_usdc"] == 0.008
    client.close()
