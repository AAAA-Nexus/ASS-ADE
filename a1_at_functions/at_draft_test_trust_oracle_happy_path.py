# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_trust_oracle_happy_path.py:5
# Component id: at.source.ass_ade.test_trust_oracle_happy_path
__version__ = "0.1.0"

def test_trust_oracle_happy_path(method_name, response_json):
    """Test trust oracle query methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "trust_score":
            result = client.trust_score(agent_id="agent_1")
        else:  # trust_history
            result = client.trust_history(agent_id="agent_1")
        assert result is not None
