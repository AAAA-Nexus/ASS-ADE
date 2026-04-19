# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:830
# Component id: mo.source.ass_ade.test_trust_oracle_happy_path
from __future__ import annotations

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
