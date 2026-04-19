# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_fetch_http_error.py:7
# Component id: at.source.a1_at_functions.test_fetch_http_error
from __future__ import annotations

__version__ = "0.1.0"

def test_fetch_http_error(self) -> None:
    import httpx as _httpx

    mock_response = MagicMock()
    mock_response.status_code = 404
    error = _httpx.HTTPStatusError("Not Found", request=MagicMock(), response=mock_response)

    with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
        with patch("ass_ade.a2a.httpx.get", side_effect=error):
            report = fetch_agent_card("https://bad.com")
            assert not report.valid
            assert any("404" in i.message for i in report.errors)
