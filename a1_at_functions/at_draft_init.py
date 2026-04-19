# Extracted from C:/!ass-ade/src/ass_ade/cli.py:340
# Component id: at.source.ass_ade.init
from __future__ import annotations

__version__ = "0.1.0"

def init(
    config: Path | None = CONFIG_OPTION,
    overwrite: bool = OVERWRITE_OPTION,
) -> None:
    target = config or default_config_path()
    existed = target.exists()
    write_default_config(target, overwrite=overwrite)
    if existed and not overwrite:
        console.print(f"Config already exists at {target}")
        return
    console.print(f"Wrote config to {target}")
