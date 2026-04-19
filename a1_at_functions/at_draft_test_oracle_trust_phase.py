# Extracted from C:/!ass-ade/tests/test_new_commands.py:125
# Component id: at.source.ass_ade.test_oracle_trust_phase
from __future__ import annotations

__version__ = "0.1.0"

def test_oracle_trust_phase(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.trust_phase_oracle.return_value = TrustPhaseResult(phase=1.5708, certified=True, monotonicity_preserved=True)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["oracle", "trust-phase", "agent-42", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
