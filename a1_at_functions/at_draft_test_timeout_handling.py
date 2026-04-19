# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_timeout_handling.py:5
# Component id: at.source.ass_ade.test_timeout_handling
__version__ = "0.1.0"

def test_timeout_handling():
    """Test timeout behavior."""
    def handler(request):
        raise httpx.TimeoutException("Request timeout")
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", timeout=1.0, transport=transport) as client:
        with pytest.raises(httpx.TimeoutException):
            client.get_health()
