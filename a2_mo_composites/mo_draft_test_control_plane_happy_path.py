# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:678
# Component id: mo.source.ass_ade.test_control_plane_happy_path
__version__ = "0.1.0"

def test_control_plane_happy_path(method_name, response_json):
    """Test control plane methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "authorize_action":
            result = client.authorize_action(agent_id="agent_1", action="execute")
        elif method_name == "spending_authorize":
            result = client.spending_authorize(agent_id="agent_1", amount_usdc=50.0)
        elif method_name == "spending_budget":
            result = client.spending_budget(agent_id="agent_1", total_usdc=1000.0)
        elif method_name == "lineage_record":
            result = client.lineage_record(intent="execute", constraints=[], outcome="success")
        elif method_name == "contract_verify":
            result = client.contract_verify(contract={"action": "execute"})
        elif method_name == "federation_mint":
            result = client.federation_mint(agent_id="agent_1", platforms=["a", "b"])
        elif method_name == "federation_verify":
            result = client.federation_verify(token="nxf_token_123")
        else:  # federation_portability
            result = client.federation_portability(from_platform="a", to_platform="b")
        assert result is not None
