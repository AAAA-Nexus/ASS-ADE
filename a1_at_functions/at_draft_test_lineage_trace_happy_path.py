# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_lineage_trace_happy_path.py:7
# Component id: at.source.a1_at_functions.test_lineage_trace_happy_path
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
