# Extracted from C:/!ass-ade/tests/test_search_x402.py:54
# Component id: at.source.ass_ade.test_search_calls_internal_search
from __future__ import annotations

__version__ = "0.1.0"

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
