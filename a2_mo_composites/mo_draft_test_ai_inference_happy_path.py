# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:1142
# Component id: mo.source.ass_ade.test_ai_inference_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_ai_inference_happy_path(method_name, response_json):
    """Test AI inference methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "inference":
            result = client.inference(prompt="test prompt")
        else:  # embed
            result = client.embed(values=[1.0, 2.0, 3.0])
        assert result is not None
