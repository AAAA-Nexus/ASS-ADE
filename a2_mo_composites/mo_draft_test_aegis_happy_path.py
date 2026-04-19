# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:645
# Component id: mo.source.ass_ade.test_aegis_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_aegis_happy_path(method_name, response_json):
    """Test NEXUS AEGIS methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "aegis_mcp_proxy":
            result = client.aegis_mcp_proxy(tool="execute", tool_input="action_data")
        elif method_name == "aegis_epistemic_route":
            result = client.aegis_epistemic_route(prompt="test query", model="auto")
        else:  # aegis_certify_epoch
            result = client.aegis_certify_epoch(system_id="system_1")
        assert result is not None
