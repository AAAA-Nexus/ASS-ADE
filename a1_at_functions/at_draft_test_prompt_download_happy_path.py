# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_prompt_download_happy_path.py:7
# Component id: at.source.a1_at_functions.test_prompt_download_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_prompt_download_happy_path():
    """Test prompt_download GET endpoint (returns raw dict)."""
    def handler(request):
        return httpx.Response(200, json={"prompts": [{"name": "prompt1", "text": "..."}]})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.prompt_download()
        assert isinstance(result, dict)
        assert "prompts" in result
