# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_security_threat_score_bad_json_exits_4.py:7
# Component id: at.source.a1_at_functions.test_security_threat_score_bad_json_exits_4
from __future__ import annotations

__version__ = "0.1.0"

def test_security_threat_score_bad_json_exits_4(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not json{{", encoding="utf-8")
    result = runner.invoke(
        app,
        ["security", "threat-score", str(bad_file), "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
    )
    assert result.exit_code == 4
    assert "Failed to read payload" in result.stdout
