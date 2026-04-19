# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_ratchet_status_happy_path.py:5
# Component id: at.source.ass_ade.test_ratchet_status_happy_path
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
