# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_agent_reputation_happy_path.py:5
# Component id: at.source.ass_ade.test_agent_reputation_happy_path
__version__ = "0.1.0"

def test_agent_reputation_happy_path():
    """Test agent_reputation POST endpoint (returns raw dict)."""
    def handler(request):
        return httpx.Response(200, json={"agent_id": "agent_1", "compliance": "pass", "trust": 0.95})
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.agent_reputation(agent_id="agent_1")
        assert isinstance(result, dict)
        assert "agent_id" in result
