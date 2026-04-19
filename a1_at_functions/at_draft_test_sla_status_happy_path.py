# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_sla_status_happy_path.py:7
# Component id: at.source.a1_at_functions.test_sla_status_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_sla_status_happy_path():
    """Test sla_status GET endpoint."""
    def handler(request):
        assert "/v1/sla/status/" in request.url.path
        return httpx.Response(200, json={"sla_id": "sla_123", "compliance_score": 0.99, "bond_remaining": 90.0})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.sla_status(sla_id="sla_123")
        assert result is not None
