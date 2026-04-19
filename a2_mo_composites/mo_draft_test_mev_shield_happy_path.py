# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:1213
# Component id: mo.source.ass_ade.test_mev_shield_happy_path
__version__ = "0.1.0"

def test_mev_shield_happy_path(method_name, response_json):
    """Test MEV Shield methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "mev_protect":
            result = client.mev_protect(tx_bundle=["tx1", "tx2"])
        else:  # mev_status
            result = client.mev_status(bundle_id="bundle_123")
        assert result is not None
