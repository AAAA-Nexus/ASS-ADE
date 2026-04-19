# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_new_commands_require_remote_for_local_profile.py:7
# Component id: at.source.a1_at_functions.test_new_commands_require_remote_for_local_profile
from __future__ import annotations

__version__ = "0.1.0"

def test_new_commands_require_remote_for_local_profile(
    tmp_path: Path, argv: list[str]
) -> None:
    result = runner.invoke(app, [*argv, "--config", str(_local_config(tmp_path))])
    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout
