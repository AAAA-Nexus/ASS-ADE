# Extracted from C:/!ass-ade/src/ass_ade/commands/providers.py:74
# Component id: at.source.ass_ade.providers_list
from __future__ import annotations

__version__ = "0.1.0"

def providers_list(
    config: Path | None = CONFIG_OPTION,
    all_providers: Annotated[bool, typer.Option("--all", help="Show all catalog entries, not just available ones.")] = False,
) -> None:
    """List available (or all) LLM providers with tier → model mapping."""
    _, settings = _resolve_config(config)
    config_providers = {
        name: override.model_dump() for name, override in settings.providers.items()
    }

    available = {p.name for p in detect_available_providers(config_providers)}

    table = Table(title="Free LLM Providers")
    table.add_column("Provider", style="bold")
    table.add_column("Status")
    table.add_column("Fast tier")
    table.add_column("Balanced tier")
    table.add_column("Deep tier")
    table.add_column("Auth env")

    for name, profile in FREE_PROVIDERS.items():
        if not all_providers and name not in available and not profile.local:
            continue
        if name in available:
            status = "[green]● ready[/green]"
        elif profile.local:
            status = "[yellow]● local (check if running)[/yellow]"
        else:
            status = "[dim]○ no key[/dim]"
        table.add_row(
            profile.display_name,
            status,
            profile.models_by_tier.get("fast", "—"),
            profile.models_by_tier.get("balanced", "—"),
            profile.models_by_tier.get("deep", "—"),
            profile.api_key_env or "(none)",
        )
    console.print(table)

    if not available:
        console.print(
            "\n[yellow]No cloud providers have API keys set.[/yellow]\n"
            "Run [bold]ass-ade providers env[/bold] to see signup URLs + env-var hints.\n"
            "Or run [bold]ollama serve[/bold] locally for a no-key fallback."
        )

    # Show active fallback chain
    chain = list(settings.provider_fallback_chain) or DEFAULT_FALLBACK_CHAIN
    console.print(f"\n[bold]Fallback chain:[/bold] {' → '.join(chain[:8])}{'...' if len(chain) > 8 else ''}")
    if settings.tier_policy:
        console.print(f"[bold]Tier policy:[/bold] {dict(settings.tier_policy)}")
