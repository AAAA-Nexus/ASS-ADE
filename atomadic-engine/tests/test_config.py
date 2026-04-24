from pathlib import Path

from ass_ade.config import AssAdeConfig, default_config_path, load_config, write_default_config


def test_default_config_path_uses_workspace_root(tmp_path: Path) -> None:
    assert default_config_path(tmp_path) == tmp_path / ".ass-ade" / "config.json"


def test_write_and_load_config_round_trip(tmp_path: Path, monkeypatch) -> None:
    # Isolate from any process-level AAAA_NEXUS_API_KEY (tests run from repo
    # root may have hydrated the project's .env into os.environ).
    monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
    target = tmp_path / ".ass-ade" / "config.json"
    expected = AssAdeConfig(profile="hybrid", agent_id="agent-77")

    write_default_config(target, config=expected, overwrite=True)
    actual = load_config(target)

    assert actual == expected


def test_load_config_honors_env_config_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
    target = tmp_path / ".ass-ade" / "config.json"
    expected = AssAdeConfig(profile="premium", agent_id="agent-env")
    write_default_config(target, config=expected, overwrite=True)
    monkeypatch.setenv("ASS_ADE_CONFIG", str(target))

    actual = load_config()

    assert actual == expected
