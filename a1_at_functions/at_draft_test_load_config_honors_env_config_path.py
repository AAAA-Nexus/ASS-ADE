# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_load_config_honors_env_config_path.py:7
# Component id: at.source.a1_at_functions.test_load_config_honors_env_config_path
from __future__ import annotations

__version__ = "0.1.0"

def test_load_config_honors_env_config_path(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("AAAA_NEXUS_API_KEY", raising=False)
    target = tmp_path / ".ass-ade" / "config.json"
    expected = AssAdeConfig(profile="premium", agent_id="agent-env")
    write_default_config(target, config=expected, overwrite=True)
    monkeypatch.setenv("ASS_ADE_CONFIG", str(target))

    actual = load_config()

    assert actual == expected
