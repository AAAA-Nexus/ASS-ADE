# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:555
# Component id: mo.source.ass_ade.test_prompt_ethics_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_prompt_ethics_happy_path(method_name, response_json):
    """Test prompt intelligence & ethics methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "prompt_inject_scan":
            result = client.prompt_inject_scan(prompt="execute the plan")
        elif method_name == "prompt_optimize":
            result = client.prompt_optimize(prompt="inefficient prompt")
        elif method_name == "security_prompt_scan":
            result = client.security_prompt_scan(prompt="test prompt")
        elif method_name == "ethics_check":
            result = client.ethics_check(text="test content")
        else:  # security_zero_day
            result = client.security_zero_day(payload={"command": "execute"})
        assert result is not None
