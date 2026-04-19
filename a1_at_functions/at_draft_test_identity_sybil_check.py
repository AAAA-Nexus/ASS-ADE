# Extracted from C:/!ass-ade/tests/test_new_commands.py:871
# Component id: at.source.ass_ade.test_identity_sybil_check
from __future__ import annotations

__version__ = "0.1.0"

def test_identity_sybil_check(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.sybil_check.return_value = SybilCheckResult(sybil_risk="low", score=0.1)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["identity", "sybil-check", "agent-1",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "low" in result.stdout
