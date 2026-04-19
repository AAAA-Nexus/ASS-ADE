# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:357
# Component id: mo.source.ass_ade.test_escrow_status_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_escrow_status_happy_path():
    """Test escrow_status GET endpoint."""
    def handler(request):
        assert "/v1/escrow/status/" in request.url.path
        return httpx.Response(200, json={"escrow_id": "escrow_123", "status": "locked", "amount": 100.0})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.escrow_status(escrow_id="escrow_123")
        assert result is not None
