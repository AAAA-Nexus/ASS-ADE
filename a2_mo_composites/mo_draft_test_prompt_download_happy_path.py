# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:575
# Component id: mo.source.ass_ade.test_prompt_download_happy_path
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
