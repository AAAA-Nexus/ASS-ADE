# Extracted from C:/!ass-ade/src/ass_ade/config.py:50
# Component id: at.source.ass_ade.default_config_path
from __future__ import annotations

__version__ = "0.1.0"

def default_config_path(base_dir: Path | None = None) -> Path:
    root = base_dir or Path.cwd()
    return root / ".ass-ade" / "config.json"
