# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:771
# Component id: mo.source.ass_ade.test_consensus_result_happy_path
__version__ = "0.1.0"

def test_consensus_result_happy_path():
    """Test consensus_result GET endpoint."""
    def handler(request):
        assert "/v1/consensus/session/" in request.url.path and "/result" in request.url.path
        return httpx.Response(200, json={"session_id": "session_123", "winning_output": "output", "confidence": 0.95})
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.consensus_result(session_id="session_123")
        assert result is not None
