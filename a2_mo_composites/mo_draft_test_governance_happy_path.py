# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:1008
# Component id: mo.source.ass_ade.test_governance_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_governance_happy_path(method_name, response_json):
    """Test governance methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "governance_vote":
            result = client.governance_vote(agent_id="agent_1", proposal_id="prop_123", vote="yes", weight=1.0)
        else:  # ethics_compliance
            result = client.ethics_compliance(system_description="system desc")
        assert result is not None
