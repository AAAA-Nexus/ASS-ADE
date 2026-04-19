# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_hybrid_config.py:7
# Component id: at.source.a1_at_functions.hybrid_config
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
