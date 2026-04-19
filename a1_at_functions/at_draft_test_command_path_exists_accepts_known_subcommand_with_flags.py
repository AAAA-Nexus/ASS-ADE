# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_command_path_exists_accepts_known_subcommand_with_flags.py:7
# Component id: at.source.a1_at_functions.test_command_path_exists_accepts_known_subcommand_with_flags
from __future__ import annotations

__version__ = "0.1.0"

def test_command_path_exists_accepts_known_subcommand_with_flags(tmp_path: Path) -> None:
    assert command_path_exists(
        ["protocol", "evolution-record", "--summary", "birth"],
        tmp_path,
    )
    assert not command_path_exists(["protocol", "made-up-command"], tmp_path)
