# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_capabilities.py:27
# Component id: at.source.ass_ade.test_command_path_exists_accepts_known_subcommand_with_flags
__version__ = "0.1.0"

def test_command_path_exists_accepts_known_subcommand_with_flags(tmp_path: Path) -> None:
    assert command_path_exists(
        ["protocol", "evolution-record", "--summary", "birth"],
        tmp_path,
    )
    assert not command_path_exists(["protocol", "made-up-command"], tmp_path)
