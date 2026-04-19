# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_defi_risk_score.py:7
# Component id: at.source.a1_at_functions.test_defi_risk_score
from __future__ import annotations

__version__ = "0.1.0"

def test_defi_risk_score(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.defi_risk_score.return_value = DefiRiskScore(risk_score=0.3, risk_level="low")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["defi", "risk-score", "aave",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
