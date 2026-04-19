# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/commands/providers.py:320
# Component id: at.source.ass_ade.providers_set_chain
__version__ = "0.1.0"

def providers_set_chain(
    chain: Annotated[str, typer.Argument(help="Comma-separated provider names (e.g., 'groq,gemini,ollama').")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Override the provider fallback chain."""
    target, settings = _resolve_config(config)
    names = [n.strip() for n in chain.split(",") if n.strip()]
    invalid = [n for n in names if get_provider(n) is None]
    if invalid:
        console.print(f"[red]Unknown providers:[/red] {', '.join(invalid)}")
        raise typer.Exit(code=1)
    settings.provider_fallback_chain = names
    _save_config(target, settings)
    console.print(f"[green]✓[/green] Fallback chain: {' → '.join(names)}")
