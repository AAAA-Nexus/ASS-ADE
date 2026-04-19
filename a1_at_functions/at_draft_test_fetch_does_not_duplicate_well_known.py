# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:159
# Component id: at.source.ass_ade.test_fetch_does_not_duplicate_well_known
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
