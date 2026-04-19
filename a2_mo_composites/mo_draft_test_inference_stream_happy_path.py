# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:1156
# Component id: mo.source.ass_ade.test_inference_stream_happy_path
__version__ = "0.1.0"

def test_inference_stream_happy_path():
    """Test inference_stream (streaming endpoint)."""
    def handler(request):
        assert request.method == "POST"
        return httpx.Response(200, text="stream1\nstream2\nstream3\n")
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        chunks = list(client.inference_stream(prompt="test prompt"))
        assert len(chunks) > 0
