# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_nexus_client_comprehensive.py:981
# Component id: mo.source.ass_ade.test_data_tools_happy_path
__version__ = "0.1.0"

def test_data_tools_happy_path(method_name, response_json):
    """Test data tools methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)
    
    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "data_validate_json":
            result = client.data_validate_json(data={"key": "value"}, schema={})
        elif method_name == "data_format_convert":
            result = client.data_format_convert(data="data", from_format="json", to_format="csv")
        else:  # data_convert
            result = client.data_convert(content="content", target_format="csv")
        assert result is not None
