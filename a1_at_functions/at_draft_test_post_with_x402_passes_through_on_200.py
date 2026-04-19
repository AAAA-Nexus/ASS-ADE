# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_post_with_x402_passes_through_on_200.py:7
# Component id: at.source.a1_at_functions.test_post_with_x402_passes_through_on_200
from __future__ import annotations

__version__ = "0.1.0"

def test_post_with_x402_passes_through_on_200(self) -> None:
    """_post_with_x402 should return normal response on 200."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"trust_score": 0.95})

    transport = httpx.MockTransport(handler)
    client = NexusClient(base_url="https://test.atomadic.tech", transport=transport)
    result = client._post_with_x402("/v1/trust/score", {"agent_id": "test"})
    assert result == {"trust_score": 0.95}
    client.close()
