# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_http_errors_raise_exception.py:5
# Component id: at.source.ass_ade.test_http_errors_raise_exception
__version__ = "0.1.0"

def test_http_errors_raise_exception(status_code, expected_exception):
    """Test that HTTP errors raise exceptions."""
    def handler(request):
        return httpx.Response(status_code, json={"error": f"Error {status_code}"})
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        with pytest.raises(expected_exception):
            client.get_health()
