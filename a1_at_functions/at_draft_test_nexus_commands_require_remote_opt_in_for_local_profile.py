# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli.py:23
# Component id: at.source.ass_ade.test_nexus_commands_require_remote_opt_in_for_local_profile
__version__ = "0.1.0"

def test_nexus_commands_require_remote_opt_in_for_local_profile(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["nexus", "overview", "--config", str(config_path)])

    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout
