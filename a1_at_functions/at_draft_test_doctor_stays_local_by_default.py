# Extracted from C:/!ass-ade/tests/test_cli.py:12
# Component id: at.source.ass_ade.test_doctor_stays_local_by_default
from __future__ import annotations

__version__ = "0.1.0"

def test_doctor_stays_local_by_default(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["doctor", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "Remote Probe" in result.stdout
    assert "disabled" in result.stdout
