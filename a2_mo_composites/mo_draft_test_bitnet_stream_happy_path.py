# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:1118
# Component id: mo.source.ass_ade.test_bitnet_stream_happy_path
from __future__ import annotations

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
