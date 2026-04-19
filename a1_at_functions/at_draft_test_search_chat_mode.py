# Extracted from C:/!ass-ade/tests/test_search_x402.py:74
# Component id: at.source.ass_ade.test_search_chat_mode
from __future__ import annotations

__version__ = "0.1.0"

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
