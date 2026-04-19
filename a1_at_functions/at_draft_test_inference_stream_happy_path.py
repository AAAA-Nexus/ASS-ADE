# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_inference_stream_happy_path.py:7
# Component id: at.source.a1_at_functions.test_inference_stream_happy_path
from __future__ import annotations

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
