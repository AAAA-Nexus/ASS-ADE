# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:704
# Component id: mo.source.ass_ade.test_lineage_trace_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_lineage_trace_happy_path():
    """Test lineage_trace GET endpoint."""
    def handler(request):
        assert "/v1/lineage/trace/" in request.url.path
        return httpx.Response(200, json={"record_id": "record_123", "chain": [], "verified": True})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.lineage_trace(record_id="record_123")
        assert result is not None
