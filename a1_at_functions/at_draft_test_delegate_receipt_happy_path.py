# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_delegate_receipt_happy_path.py:5
# Component id: at.source.ass_ade.test_delegate_receipt_happy_path
__version__ = "0.1.0"

def test_delegate_receipt_happy_path():
    """Test delegate_receipt GET endpoint."""
    def handler(request):
        assert "/v1/delegate/receipt/" in request.url.path
        return httpx.Response(200, json={"receipt_id": "receipt_123", "signature": "sig_xyz"})
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.delegate_receipt(receipt_id="receipt_123")
        assert result is not None
