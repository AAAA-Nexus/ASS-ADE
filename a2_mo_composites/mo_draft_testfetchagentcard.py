# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:127
# Component id: mo.source.ass_ade.testfetchagentcard
__version__ = "0.1.0"

class TestFetchAgentCard:
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

    def test_fetch_network_error(self) -> None:
        import httpx as _httpx

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", side_effect=_httpx.ConnectError("refused")):
                report = fetch_agent_card("https://unreachable.com")
                assert not report.valid
                assert any("Network" in i.message for i in report.errors)

    def test_fetch_invalid_json(self) -> None:
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", return_value=mock_response):
                report = fetch_agent_card("https://bad-json.com")
                assert not report.valid
                assert any("JSON" in i.message for i in report.errors)
