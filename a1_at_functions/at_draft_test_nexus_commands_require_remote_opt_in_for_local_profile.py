# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_nexus_commands_require_remote_opt_in_for_local_profile.py:7
# Component id: at.source.a1_at_functions.test_nexus_commands_require_remote_opt_in_for_local_profile
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_commands_require_remote_opt_in_for_local_profile(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["nexus", "overview", "--config", str(config_path)])

    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout
