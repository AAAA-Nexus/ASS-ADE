# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_post_with_x402_raises_on_other_errors.py:7
# Component id: at.source.a1_at_functions.test_post_with_x402_raises_on_other_errors
from __future__ import annotations

__version__ = "0.1.0"

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
