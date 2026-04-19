# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:307
# Component id: mo.source.ass_ade.test_identity_auth_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_identity_auth_happy_path(method_name, response_json):
    """Test identity & auth methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "identity_verify":
            result = client.identity_verify(actor="agent_1")
        elif method_name == "sybil_check":
            result = client.sybil_check(actor="agent_1")
        else:  # zero_trust_auth
            result = client.zero_trust_auth(agent_id=324, endpoint="/execute", capability="run")
        assert result is not None
