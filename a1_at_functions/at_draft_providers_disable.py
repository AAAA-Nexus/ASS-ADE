# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/commands/providers.py:248
# Component id: at.source.ass_ade.providers_disable
__version__ = "0.1.0"

def providers_disable(
    name: Annotated[str, typer.Argument(help="Provider name to disable.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Disable a provider (exclude from the fallback chain)."""
    _set_enabled(name, False, config)
