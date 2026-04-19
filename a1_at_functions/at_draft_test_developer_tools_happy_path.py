# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_developer_tools_happy_path.py:7
# Component id: at.source.a1_at_functions.test_developer_tools_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_developer_tools_happy_path(method_name, response_json):
    """Test developer tools methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "crypto_toolkit":
            result = client.crypto_toolkit(data="data_to_hash")
        else:  # dev_starter
            result = client.dev_starter(project_name="my_project", language="python")
        assert result is not None
