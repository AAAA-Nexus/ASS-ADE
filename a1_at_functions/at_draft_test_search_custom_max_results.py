# Extracted from C:/!ass-ade/tests/test_search_x402.py:90
# Component id: at.source.ass_ade.test_search_custom_max_results
from __future__ import annotations

__version__ = "0.1.0"

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
