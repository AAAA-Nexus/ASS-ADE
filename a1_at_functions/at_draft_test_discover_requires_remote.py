# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testa2adiscovercli.py:21
# Component id: at.source.ass_ade.test_discover_requires_remote
__version__ = "0.1.0"

    def test_discover_requires_remote(self, tmp_path: Path) -> None:
        config_path = tmp_path / ".ass-ade" / "config.json"
        write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)
        result = runner.invoke(app, ["a2a", "discover", "search", "--config", str(config_path)])
        assert result.exit_code == 2
        assert "disabled in the local profile" in result.stdout
