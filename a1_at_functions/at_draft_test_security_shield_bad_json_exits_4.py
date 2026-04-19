# Extracted from C:/!ass-ade/tests/test_new_commands.py:530
# Component id: at.source.ass_ade.test_security_shield_bad_json_exits_4
from __future__ import annotations

__version__ = "0.1.0"

def test_security_shield_bad_json_exits_4(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{broken", encoding="utf-8")
    result = runner.invoke(
        app,
        ["security", "shield", str(bad_file), "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
    )
    assert result.exit_code == 4
    assert "Failed to read payload" in result.stdout
