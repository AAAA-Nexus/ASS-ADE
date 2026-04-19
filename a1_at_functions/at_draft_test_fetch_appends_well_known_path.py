# Extracted from C:/!ass-ade/tests/test_a2a.py:146
# Component id: at.source.ass_ade.test_fetch_appends_well_known_path
from __future__ import annotations

__version__ = "0.1.0"

def test_fetch_appends_well_known_path(self) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"name": "Test"}

    with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
        with patch("ass_ade.a2a.httpx.get", return_value=mock_response) as mock_get:
            fetch_agent_card("https://example.com/")
            mock_get.assert_called_once_with(
                "https://example.com/.well-known/agent.json",
                timeout=10.0,
                follow_redirects=False,
            )
