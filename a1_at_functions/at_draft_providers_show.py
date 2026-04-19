# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_providers_show.py:7
# Component id: at.source.a1_at_functions.providers_show
from __future__ import annotations

__version__ = "0.1.0"

def providers_show(
    name: Annotated[str, typer.Argument(help="Provider name (e.g., groq, gemini).")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show details for a single provider."""
    _, settings = _resolve_config(config)
    profile = get_provider(name)
    if profile is None:
        console.print(f"[red]Unknown provider:[/red] {name}")
        console.print(f"Available: {', '.join(list_providers())}")
        raise typer.Exit(code=1)

    user_override = settings.providers.get(name)
    user_key = user_override.api_key if user_override else None
    user_models = user_override.models_by_tier if user_override else None
    user_enabled = user_override.enabled if user_override else True

    resolved_key = profile.resolve_api_key(user_key)
    available = profile.is_available(user_key)

    t = Table(title=f"Provider: {profile.display_name}")
    t.add_column("Field")
    t.add_column("Value")
    t.add_row("Name", profile.name)
    t.add_row("Base URL", (user_override.base_url if user_override and user_override.base_url else profile.base_url) or "(none)")
    t.add_row("Auth env", profile.api_key_env or "(no key)")
    t.add_row("Has key", "[green]yes[/green]" if resolved_key else "[red]no[/red]")
    t.add_row("Enabled", "[green]yes[/green]" if user_enabled else "[red]no[/red]")
    t.add_row("Available", "[green]yes[/green]" if available else "[red]no[/red]")
    t.add_row("Local", "yes" if profile.local else "no")
    t.add_row("Free tier", "yes")
    if profile.rate_limit:
        t.add_row("Rate limit", profile.rate_limit)
    if profile.signup_url:
        t.add_row("Signup", profile.signup_url)

    for tier in ("fast", "balanced", "deep"):
        default = profile.models_by_tier.get(tier, "—")
        if user_models and user_models.get(tier):
            t.add_row(f"Model ({tier})", f"{user_models[tier]} [dim](override)[/dim]")
        else:
            t.add_row(f"Model ({tier})", default)

    console.print(t)
    if profile.notes:
        console.print(f"\n[dim]{profile.notes}[/dim]")
