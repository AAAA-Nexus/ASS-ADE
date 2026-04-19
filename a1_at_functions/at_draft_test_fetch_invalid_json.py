# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:194
# Component id: at.source.ass_ade.test_fetch_invalid_json
__version__ = "0.1.0"

    def test_fetch_invalid_json(self) -> None:
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("", "", 0)

        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO):
            with patch("ass_ade.a2a.httpx.get", return_value=mock_response):
                report = fetch_agent_card("https://bad-json.com")
                assert not report.valid
                assert any("JSON" in i.message for i in report.errors)
