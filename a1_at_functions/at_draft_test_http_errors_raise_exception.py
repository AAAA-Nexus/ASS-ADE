# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_http_errors_raise_exception.py:7
# Component id: at.source.a1_at_functions.test_http_errors_raise_exception
from __future__ import annotations

__version__ = "0.1.0"

def test_http_errors_raise_exception(status_code, expected_exception):
    """Test that HTTP errors raise exceptions."""
    def handler(request):
        return httpx.Response(status_code, json={"error": f"Error {status_code}"})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        with pytest.raises(expected_exception):
            client.get_health()
