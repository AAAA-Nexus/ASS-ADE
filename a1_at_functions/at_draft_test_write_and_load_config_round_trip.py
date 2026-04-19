# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_config.py:10
# Component id: at.source.ass_ade.test_write_and_load_config_round_trip
__version__ = "0.1.0"

def test_write_and_load_config_round_trip(tmp_path: Path, monkeypatch) -> None:
    # Isolate from any process-level AAAA_NEXUS_API_KEY (tests run from repo
    # root may have hydrated the project's .env into os.environ).
    monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
    target = tmp_path / ".ass-ade" / "config.json"
    expected = AssAdeConfig(profile="hybrid", agent_id="agent-77")

    write_default_config(target, config=expected, overwrite=True)
    actual = load_config(target)

    assert actual == expected
