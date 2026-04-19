# Extracted from C:/!ass-ade/tests/test_mcp.py:14
# Component id: sy.source.ass_ade.test_mcp_tools_require_remote_opt_in_for_local_profile
from __future__ import annotations

__version__ = "0.1.0"

def test_mcp_tools_require_remote_opt_in_for_local_profile(tmp_path: Path) -> None:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="local"), overwrite=True)

    result = runner.invoke(app, ["mcp", "tools", "--config", str(config_path)])

    assert result.exit_code == 2
    assert "disabled in the local profile" in result.stdout
