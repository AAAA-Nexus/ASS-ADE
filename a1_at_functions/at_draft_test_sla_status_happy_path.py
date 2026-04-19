# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_sla_status_happy_path.py:5
# Component id: at.source.ass_ade.test_sla_status_happy_path
__version__ = "0.1.0"

def test_sla_status_happy_path():
    """Test sla_status GET endpoint."""
    def handler(request):
        assert "/v1/sla/status/" in request.url.path
        return httpx.Response(200, json={"sla_id": "sla_123", "compliance_score": 0.99, "bond_remaining": 90.0})
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.sla_status(sla_id="sla_123")
        assert result is not None
