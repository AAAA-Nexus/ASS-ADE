# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_search_x402.py:43
# Component id: mo.source.ass_ade.testsearchcommand
__version__ = "0.1.0"

class TestSearchCommand:
    def test_search_requires_session_token(self, tmp_path: Path) -> None:
        """Search should fail if ATOMADIC_SESSION_TOKEN is not set."""
        result = runner.invoke(
            app,
            ["search", "test query", "--config", str(_hybrid_config(tmp_path))],
            env={"ATOMADIC_SESSION_TOKEN": ""},
        )
        assert result.exit_code == 1
        assert "ATOMADIC_SESSION_TOKEN" in result.stdout

    def test_search_calls_internal_search(self, tmp_path: Path) -> None:
        """Search with valid session token should call internal_search."""
        mock_nx = MagicMock()
        mock_nx.internal_search.return_value = {
            "success": True,
            "result": {"search_query": "test results", "chunks": []},
        }
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["search", "Atomadic invariants", "--config", str(_hybrid_config(tmp_path))],
                env={"ATOMADIC_SESSION_TOKEN": "test-session-abc123"},
            )
        assert result.exit_code == 0
        mock_nx.internal_search.assert_called_once_with(
            query="Atomadic invariants",
            max_results=10,
            session_token="test-session-abc123",
        )

    def test_search_chat_mode(self, tmp_path: Path) -> None:
        """Search with --chat flag should call internal_search_chat."""
        mock_nx = MagicMock()
        mock_nx.internal_search_chat.return_value = {
            "success": True,
            "result": {"response": "The Atomadic codex defines..."},
        }
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["search", "what is the codex", "--chat", "--config", str(_hybrid_config(tmp_path))],
                env={"ATOMADIC_SESSION_TOKEN": "test-session-abc123"},
            )
        assert result.exit_code == 0
        mock_nx.internal_search_chat.assert_called_once()

    def test_search_custom_max_results(self, tmp_path: Path) -> None:
        """Search with --max-results should pass through to client."""
        mock_nx = MagicMock()
        mock_nx.internal_search.return_value = {"success": True, "result": {}}
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["search", "query", "--max-results", "5", "--config", str(_hybrid_config(tmp_path))],
                env={"ATOMADIC_SESSION_TOKEN": "sess-tok"},
            )
        assert result.exit_code == 0
        mock_nx.internal_search.assert_called_once_with(
            query="query", max_results=5, session_token="sess-tok"
        )
