# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_fetch_invalid_json.py:7
# Component id: at.source.a1_at_functions.test_fetch_invalid_json
from __future__ import annotations

__version__ = "0.1.0"

def test_fetch_invalid_json(self) -> None:
    mock_response = MagicMock()
    mock_response.json.side_effect = json.JSONDecodeError("", "", 0)

    with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
        with patch("ass_ade.a2a.httpx.get", return_value=mock_response):
            report = fetch_agent_card("https://bad-json.com")
            assert not report.valid
            assert any("JSON" in i.message for i in report.errors)
