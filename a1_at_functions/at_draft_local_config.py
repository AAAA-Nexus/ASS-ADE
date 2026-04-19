# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:70
# Component id: at.source.ass_ade.local_config
from __future__ import annotations

__version__ = "0.1.0"

def local_config(tmp_path: Path) -> Path:
    """Create a local profile config (remote calls require --allow-remote)."""
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(
        config_path,
        config=AssAdeConfig(profile="local"),
        overwrite=True,
    )
    return config_path
