# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:172
# Component id: at.source.ass_ade.test_fetch_http_error
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
