# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_bitnet_happy_path.py:7
# Component id: at.source.a1_at_functions.test_bitnet_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_bitnet_happy_path(method_name, response_json):
    """Test BitNet 1.58-bit inference methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "bitnet_models":
            result = client.bitnet_models()
        elif method_name == "bitnet_inference":
            result = client.bitnet_inference(prompt="test prompt")
        elif method_name == "bitnet_benchmark":
            result = client.bitnet_benchmark(model="bitnet-b1.58-2B-4T", n_tokens=100)
        elif method_name == "bitnet_quantize":
            result = client.bitnet_quantize(model_id="model_1")
        else:  # bitnet_status
            result = client.bitnet_status()
        assert result is not None
