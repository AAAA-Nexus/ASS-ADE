# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:1285
# Component id: mo.source.ass_ade.test_timeout_handling
__version__ = "0.1.0"

def test_timeout_handling():
    """Test timeout behavior."""
    def handler(request):
        raise httpx.TimeoutException("Request timeout")
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", timeout=1.0, transport=transport) as client:
        with pytest.raises(httpx.TimeoutException):
            client.get_health()
