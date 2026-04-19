# Extracted from C:/!ass-ade/tests/test_a2a.py:128
# Component id: at.source.ass_ade.test_fetch_success
from __future__ import annotations

__version__ = "0.1.0"

def test_fetch_success(self) -> None:
    card_data = {"name": "RemoteAgent", "description": "A remote agent", "url": "https://remote.com", "version": "2.0"}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = card_data

    with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
        with patch("ass_ade.a2a.httpx.get", return_value=mock_response) as mock_get:
            report = fetch_agent_card("https://remote.com")
            mock_get.assert_called_once_with(
                "https://remote.com/.well-known/agent.json",
                timeout=10.0,
                follow_redirects=False,
            )
            assert report.valid
            assert report.card is not None
            assert report.card.name == "RemoteAgent"
