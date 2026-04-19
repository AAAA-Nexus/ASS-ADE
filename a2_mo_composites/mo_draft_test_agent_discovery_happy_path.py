# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:461
# Component id: mo.source.ass_ade.test_agent_discovery_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_agent_discovery_happy_path(method_name, response_json):
    """Test agent discovery methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "discovery_search":
            result = client.discovery_search(capability="execute")
        elif method_name == "discovery_recommend":
            result = client.discovery_recommend(task="find an executor")
        else:  # discovery_registry
            result = client.discovery_registry()
        assert result is not None
