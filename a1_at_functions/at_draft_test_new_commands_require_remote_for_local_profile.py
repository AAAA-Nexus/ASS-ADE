# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_test_new_commands_require_remote_for_local_profile.py:5
# Component id: at.source.ass_ade.test_new_commands_require_remote_for_local_profile
__version__ = "0.1.0"

def test_new_commands_require_remote_for_local_profile(
    tmp_path: Path, argv: list[str]
) -> None:
    result = runner.invoke(app, [*argv, "--config", str(_local_config(tmp_path))])
    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout
