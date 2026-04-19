# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:269
# Component id: mo.source.ass_ade.test_veridelegate_happy_path
__version__ = "0.1.0"

def test_veridelegate_happy_path(method_name, response_json):
    """Test VeriDelegate UCAN methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "delegate_verify":
            result = client.delegate_verify(chain=[{"token": "token_123"}])
        else:  # delegation_validate
            result = client.delegation_validate(chain=[{"token": "token_123"}])
        assert result is not None
