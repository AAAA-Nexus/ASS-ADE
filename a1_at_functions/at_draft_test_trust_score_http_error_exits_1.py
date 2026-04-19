# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trust_score_http_error_exits_1.py:7
# Component id: at.source.a1_at_functions.test_trust_score_http_error_exits_1
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
