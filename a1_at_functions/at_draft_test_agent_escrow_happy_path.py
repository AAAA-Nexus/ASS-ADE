# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_agent_escrow_happy_path.py:7
# Component id: at.source.a1_at_functions.test_agent_escrow_happy_path
from __future__ import annotations

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
