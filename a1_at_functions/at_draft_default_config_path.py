# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_default_config_path.py:7
# Component id: at.source.a1_at_functions.default_config_path
from __future__ import annotations

__version__ = "0.1.0"

def default_config_path(base_dir: Path | None = None) -> Path:
    root = base_dir or Path.cwd()
    return root / ".ass-ade" / "config.json"
