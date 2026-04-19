# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:196
# Component id: mo.source.ass_ade.test_ratchet_status_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_ratchet_status_happy_path():
    """Test ratchet_status GET endpoint."""
    def handler(request):
        assert "/v1/ratchet/status/" in request.url.path
        return httpx.Response(200, json={"epoch": 5, "remaining_calls": 1000})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.ratchet_status(session_id="ratchet_abc123")
        assert result is not None
