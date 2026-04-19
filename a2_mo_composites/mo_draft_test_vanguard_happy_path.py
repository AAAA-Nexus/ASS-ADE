# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:1182
# Component id: mo.source.ass_ade.test_vanguard_happy_path
__version__ = "0.1.0"

def test_vanguard_happy_path(method_name, response_json):
    """Test VANGUARD methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "vanguard_redteam":
            result = client.vanguard_redteam(agent_id="agent_1", target="target_endpoint")
        elif method_name == "vanguard_mev_route":
            result = client.vanguard_mev_route(agent_id="agent_1", intent={})
        elif method_name == "vanguard_govern_session":
            result = client.vanguard_govern_session(agent_id="agent_1", session_key="key_123")
        elif method_name == "vanguard_start_session":
            result = client.vanguard_start_session(agent_id="agent_1")
        else:  # vanguard_lock_and_verify
            result = client.vanguard_lock_and_verify(payer_agent_id="agent_1", payee_agent_id="agent_2", amount_micro_usdc=1000000)
        assert result is not None
