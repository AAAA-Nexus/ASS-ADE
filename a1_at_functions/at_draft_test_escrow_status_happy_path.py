# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_escrow_status_happy_path.py:5
# Component id: at.source.ass_ade.test_escrow_status_happy_path
__version__ = "0.1.0"

def test_escrow_status_happy_path():
    """Test escrow_status GET endpoint."""
    def handler(request):
        assert "/v1/escrow/status/" in request.url.path
        return httpx.Response(200, json={"escrow_id": "escrow_123", "status": "locked", "amount": 100.0})
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.escrow_status(escrow_id="escrow_123")
        assert result is not None
