# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trust_score.py:7
# Component id: at.source.a1_at_functions.test_trust_score
from __future__ import annotations

__version__ = "0.1.0"

def test_trust_score(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.trust_score.return_value = TrustScore(agent_id="agent-1", score=0.92, tier="gold", certified_monotonic=True)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["trust", "score", "agent-1", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "gold" in result.stdout
    assert "0.92" in result.stdout
