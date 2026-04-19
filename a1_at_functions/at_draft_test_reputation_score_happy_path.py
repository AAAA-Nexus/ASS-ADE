# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_reputation_score_happy_path.py:5
# Component id: at.source.ass_ade.test_reputation_score_happy_path
__version__ = "0.1.0"

def test_reputation_score_happy_path():
    """Test reputation_score GET endpoint."""
    def handler(request):
        assert "/v1/reputation/score/" in request.url.path
        return httpx.Response(200, json={"agent_id": "agent_1", "tier": "gold", "fee_multiplier": 0.8})
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.reputation_score(agent_id="agent_1")
        assert result is not None
