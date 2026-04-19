# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:783
# Component id: mo.source.ass_ade.test_quota_status_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_quota_status_happy_path():
    """Test quota_status GET endpoint."""
    def handler(request):
        assert "/v1/quota/tree/" in request.url.path and "/status" in request.url.path
        return httpx.Response(200, json={"tree_id": "tree_123", "remaining_budget": 9900, "alerts": []})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.quota_status(tree_id="tree_123")
        assert result is not None
