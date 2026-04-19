# Extracted from C:/!ass-ade/tests/test_new_commands.py:471
# Component id: at.source.ass_ade.test_trust_score_http_error_exits_1
from __future__ import annotations

__version__ = "0.1.0"

def test_trust_score_http_error_exits_1(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.trust_score.side_effect = _http_error(402)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["trust", "score", "agent-x", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 1
    assert "x402" in result.stdout
