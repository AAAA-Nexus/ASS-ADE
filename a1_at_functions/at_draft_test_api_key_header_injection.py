# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_api_key_header_injection.py:7
# Component id: at.source.a1_at_functions.test_api_key_header_injection
from __future__ import annotations

__version__ = "0.1.0"

def test_api_key_header_injection():
    """Test that api_key is safely injected into headers."""
    api_key = "test_api_key_123"

    def handler(request):
        assert "Authorization" in request.headers
        assert request.headers["Authorization"] == f"Bearer {api_key}"
        assert request.headers["X-API-Key"] == api_key
        return httpx.Response(200, json={"status": "ok"})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", api_key=api_key, transport=transport) as client:
        result = client.get_health()
        assert result is not None
