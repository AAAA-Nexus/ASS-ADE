# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_memory_fence_audit_happy_path.py:7
# Component id: at.source.a1_at_functions.test_memory_fence_audit_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_memory_fence_audit_happy_path():
    """Test memory_fence_audit GET endpoint."""
    def handler(request):
        assert "/v1/memory/fence/" in request.url.path and "/audit" in request.url.path
        return httpx.Response(200, json={"fence_id": "fence_123", "access_count": 10})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.memory_fence_audit(fence_id="fence_123")
        assert result is not None
