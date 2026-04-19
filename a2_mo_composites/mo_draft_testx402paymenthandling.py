# Extracted from C:/!ass-ade/tests/test_search_x402.py:111
# Component id: mo.source.ass_ade.testx402paymenthandling
from __future__ import annotations

__version__ = "0.1.0"

class TestX402PaymentHandling:
    def _make_client(self) -> NexusClient:
        transport = httpx.MockTransport(lambda req: httpx.Response(200, json={}))
        return NexusClient(base_url="https://test.atomadic.tech", transport=transport)

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

    def test_handle_x402_fallback_fields(self) -> None:
        """handle_x402 should handle alternative field names."""
        client = self._make_client()
        mock_response = httpx.Response(
            402,
            json={
                "price_usdc": 0.04,
                "treasury": "0xABC123",
                "message": "Insufficient credits",
            },
        )
        result = client.handle_x402(mock_response)
        assert result["payment_required"] is True
        assert result["amount_usdc"] == 0.04
        assert result["treasury"] == "0xABC123"
        assert result["detail"] == "Insufficient credits"
        client.close()

    def test_handle_x402_empty_body(self) -> None:
        """handle_x402 should handle empty or malformed 402 body."""
        client = self._make_client()
        mock_response = httpx.Response(402, text="Payment Required")
        result = client.handle_x402(mock_response)
        assert result["payment_required"] is True
        assert result["amount_usdc"] == 0
        assert result["network"] == "base"
        client.close()

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

    def test_post_with_x402_passes_through_on_200(self) -> None:
        """_post_with_x402 should return normal response on 200."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"trust_score": 0.95})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        result = client._post_with_x402("/v1/trust/score", {"agent_id": "test"})
        assert result == {"trust_score": 0.95}
        client.close()

    def test_post_with_x402_raises_on_other_errors(self) -> None:
        """_post_with_x402 should raise on non-402 errors (401, 500, etc.)."""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, json={"error": "unauthorized"})

        transport = httpx.MockTransport(handler)
        client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
        from ass_ade.nexus.errors import NexusAuthError
        with pytest.raises(NexusAuthError):
            client._post_with_x402("/v1/trust/score")
        client.close()
