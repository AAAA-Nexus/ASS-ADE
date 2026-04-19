# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trust_oracle_happy_path.py:7
# Component id: at.source.a1_at_functions.test_trust_oracle_happy_path
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
