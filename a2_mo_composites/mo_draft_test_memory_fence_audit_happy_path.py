# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:807
# Component id: mo.source.ass_ade.test_memory_fence_audit_happy_path
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
