# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/commands/providers.py:269
# Component id: at.source.ass_ade.providers_set_tier
__version__ = "0.1.0"

def providers_set_tier(
    tier: Annotated[str, typer.Argument(help="Tier name: fast / balanced / deep (or haiku / sonnet / opus).")],
    provider: Annotated[str, typer.Argument(help="Provider to use for this tier.")],
    model: Annotated[str | None, typer.Option(help="Override the model id for this (provider, tier) pair.")] = None,
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Pin a tier to a specific provider (e.g., 'balanced → groq')."""
    canonical = resolve_tier(tier)
    if canonical not in ("fast", "balanced", "deep"):
        console.print(f"[red]Unknown tier:[/red] {tier}")
        raise typer.Exit(code=1)
    profile = get_provider(provider)
    if profile is None:
        console.print(f"[red]Unknown provider:[/red] {provider}")
        raise typer.Exit(code=1)
    target, settings = _resolve_config(config)
    settings.tier_policy[canonical] = provider
    if model:
        current = settings.providers.get(provider) or ProviderOverride()
        models = dict(current.models_by_tier or {})
        models[canonical] = model
        current.models_by_tier = models
        settings.providers[provider] = current
    _save_config(target, settings)
    console.print(f"[green]✓[/green] {canonical} → {provider}" + (f" (model={model})" if model else ""))
