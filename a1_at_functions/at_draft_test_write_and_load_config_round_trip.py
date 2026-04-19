# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_write_and_load_config_round_trip.py:7
# Component id: at.source.a1_at_functions.test_write_and_load_config_round_trip
from __future__ import annotations

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
