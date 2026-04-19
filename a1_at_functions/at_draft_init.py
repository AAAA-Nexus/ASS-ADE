# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_init.py:7
# Component id: at.source.a1_at_functions.init
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
