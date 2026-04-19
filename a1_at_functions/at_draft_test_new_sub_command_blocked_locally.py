# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_new_sub_command_blocked_locally.py:7
# Component id: at.source.a1_at_functions.test_new_sub_command_blocked_locally
from __future__ import annotations

__version__ = "0.1.0"

def test_new_sub_command_blocked_locally(tmp_path: Path, argv: list[str]) -> None:
    """New sub-commands must exit code 2 without --allow-remote in local profile."""
    config = _local_config(tmp_path)
    result = runner.invoke(app, argv + ["--config", str(config)])
    assert result.exit_code == 2
