# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_ratchet_status_happy_path.py:7
# Component id: at.source.a1_at_functions.test_ratchet_status_happy_path
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
