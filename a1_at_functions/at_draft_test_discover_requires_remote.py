# Extracted from C:/!ass-ade/tests/test_a2a_cli.py:84
# Component id: at.source.ass_ade.test_discover_requires_remote
from __future__ import annotations

__version__ = "0.1.0"

def test_discover_requires_remote(self, tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)
    result = runner.invoke(app, ["a2a", "discover", "search", "--config", str(config_path)])
    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout
