# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_bitnet_happy_path.py:5
# Component id: at.source.ass_ade.test_bitnet_happy_path
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
