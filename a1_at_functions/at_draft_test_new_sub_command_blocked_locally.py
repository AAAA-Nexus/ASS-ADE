# Extracted from C:/!ass-ade/tests/test_new_commands.py:607
# Component id: at.source.ass_ade.test_new_sub_command_blocked_locally
from __future__ import annotations

__version__ = "0.1.0"

def test_new_sub_command_blocked_locally(tmp_path: Path, argv: list[str]) -> None:
    """New sub-commands must exit code 2 without --allow-remote in local profile."""
    config = _local_config(tmp_path)
    result = runner.invoke(app, argv + ["--config", str(config)])
    assert result.exit_code == 2
