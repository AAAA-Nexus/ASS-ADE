# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_config.py:23
# Component id: at.source.ass_ade.test_load_config_honors_env_config_path
__version__ = "0.1.0"

def test_load_config_honors_env_config_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
    target = tmp_path / ".ass-ade" / "config.json"
    expected = AssAdeConfig(profile="premium", agent_id="agent-env")
    write_default_config(target, config=expected, overwrite=True)
    monkeypatch.setenv("ASS_ADE_CONFIG", str(target))

    actual = load_config()

    assert actual == expected
