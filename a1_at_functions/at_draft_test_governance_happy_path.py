# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_governance_happy_path.py:7
# Component id: at.source.a1_at_functions.test_governance_happy_path
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
