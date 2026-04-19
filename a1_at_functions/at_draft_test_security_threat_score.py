# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_security_threat_score.py:7
# Component id: at.source.a1_at_functions.test_security_threat_score
from __future__ import annotations

__version__ = "0.1.0"

def test_security_threat_score(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.threat_score.return_value = ThreatScore(threat_level="low", score=0.1)
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps({"data": "benign"}), encoding="utf-8")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["security", "threat-score", str(payload_file), "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "low" in result.stdout
