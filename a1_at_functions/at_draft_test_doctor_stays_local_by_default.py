# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_doctor_stays_local_by_default.py:7
# Component id: at.source.a1_at_functions.test_doctor_stays_local_by_default
from __future__ import annotations

__version__ = "0.1.0"

def test_doctor_stays_local_by_default(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["doctor", "--config", str(config_path)])

    assert result.exit_code == 0
    assert "Remote Probe" in result.stdout
    assert "disabled" in result.stdout
