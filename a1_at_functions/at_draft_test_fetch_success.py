# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_fetch_success.py:7
# Component id: at.source.a1_at_functions.test_fetch_success
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
