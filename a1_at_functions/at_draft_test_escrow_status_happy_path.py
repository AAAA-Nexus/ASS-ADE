# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_escrow_status_happy_path.py:7
# Component id: at.source.a1_at_functions.test_escrow_status_happy_path
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
