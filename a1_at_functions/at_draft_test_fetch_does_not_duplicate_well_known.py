# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_fetch_does_not_duplicate_well_known.py:7
# Component id: at.source.a1_at_functions.test_fetch_does_not_duplicate_well_known
from __future__ import annotations

__version__ = "0.1.0"

def test_fetch_does_not_duplicate_well_known(self) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"name": "Test"}

    with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
        with patch("ass_ade.a2a.httpx.get", return_value=mock_response) as mock_get:
            fetch_agent_card("https://example.com/.well-known/agent.json")
            mock_get.assert_called_once_with(
                "https://example.com/.well-known/agent.json",
                timeout=10.0,
                follow_redirects=False,
            )
