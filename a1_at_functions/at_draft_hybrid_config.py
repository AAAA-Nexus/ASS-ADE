# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:58
# Component id: at.source.ass_ade.hybrid_config
from __future__ import annotations

__version__ = "0.1.0"

def hybrid_config(tmp_path: Path) -> Path:
    """Create a hybrid profile config (allows remote calls)."""
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(
        config_path,
        config=AssAdeConfig(profile="hybrid"),
        overwrite=True,
    )
    return config_path
