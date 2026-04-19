# Extracted from C:/!ass-ade/tests/test_ssrf_protection.py:98
# Component id: at.source.ass_ade.test_appends_well_known_path
from __future__ import annotations

__version__ = "0.1.0"

def test_appends_well_known_path(self) -> None:
    """Fetching from a URL without /.well-known/agent.json should auto-append it."""
    # Mock httpx.get to verify the right URL is called
    with mock.patch("ass_ade.a2a.httpx.get") as mock_get:
        mock_response = mock.MagicMock()
        mock_response.json.return_value = {"name": "TestAgent"}
        mock_get.return_value = mock_response

        # This should work and return valid=False because the JSON is incomplete
        # but we mainly care about the URL transformation
        fetch_agent_card("https://example.com")

        # Verify that the .well-known path was appended
        called_url = mock_get.call_args[0][0]
        assert called_url.endswith("/.well-known/agent.json")
