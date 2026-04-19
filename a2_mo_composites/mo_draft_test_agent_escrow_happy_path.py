# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:336
# Component id: mo.source.ass_ade.test_agent_escrow_happy_path
__version__ = "0.1.0"

def test_agent_escrow_happy_path(method_name, response_json):
    """Test agent escrow methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "escrow_create":
            result = client.escrow_create(
                amount_usdc=100.0, sender="agent_1", receiver="agent_2",
                conditions=["completed"]
            )
        elif method_name == "escrow_release":
            result = client.escrow_release(escrow_id="escrow_123", proof="completion_proof")
        elif method_name == "escrow_dispute":
            result = client.escrow_dispute(escrow_id="escrow_123", evidence="proof_of_failure")
        else:  # escrow_arbitrate
            result = client.escrow_arbitrate(escrow_id="escrow_123", vote="release")
        assert result is not None
