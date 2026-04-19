# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:339
# Component id: at.source.ass_ade.init
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
