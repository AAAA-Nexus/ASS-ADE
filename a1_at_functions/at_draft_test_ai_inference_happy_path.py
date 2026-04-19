# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_ai_inference_happy_path.py:5
# Component id: at.source.ass_ade.test_ai_inference_happy_path
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
