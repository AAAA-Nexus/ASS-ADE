# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_timeout_handling.py:7
# Component id: at.source.a1_at_functions.test_timeout_handling
from __future__ import annotations

__version__ = "0.1.0"

def test_timeout_handling():
    """Test timeout behavior."""
    def handler(request):
        raise httpx.TimeoutException("Request timeout")

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", timeout=1.0, transport=transport) as client:
        with pytest.raises(httpx.TimeoutException):
            client.get_health()
