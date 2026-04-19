# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_bitnet_stream_happy_path.py:5
# Component id: at.source.ass_ade.test_bitnet_stream_happy_path
__version__ = "0.1.0"

def test_bitnet_stream_happy_path():
    """Test bitnet_stream (streaming endpoint)."""
    def handler(request):
        assert request.method == "POST"
        # Return streaming response
        return httpx.Response(200, text="chunk1\nchunk2\nchunk3\n")
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        chunks = list(client.bitnet_stream(prompt="test prompt"))
        assert len(chunks) > 0
