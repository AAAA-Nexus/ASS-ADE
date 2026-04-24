"""Providers command group — manage free LLM provider configuration."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Annotated

import httpx
import typer
from rich.console import Console
from rich.table import Table

from ass_ade.agent.providers import (
    DEFAULT_FALLBACK_CHAIN,
    FREE_PROVIDERS,
    detect_available_providers,
    get_provider,
    list_providers,
    resolve_tier,
)
from ass_ade.config import (
    AssAdeConfig,
    ProviderOverride,
    default_config_path,
    load_config,
)

console = Console()

CONFIG_OPTION = typer.Option(None, help="Path to the ASS-ADE config file.")


def register(app: typer.Typer) -> None:
    """Register providers commands on the provided app."""
    app.command("list")(providers_list)
    app.command("show")(providers_show)
    app.command("test")(providers_test)
    app.command("enable")(providers_enable)
    app.command("disable")(providers_disable)
    app.command("set-tier")(providers_set_tier)
    app.command("set-key")(providers_set_key)
    app.command("set-chain")(providers_set_chain)
    app.command("env")(providers_env)

    # Register the new set-default command
    app.command("set-default")(providers_set_default)
def providers_set_default(
    provider: Annotated[str, typer.Argument(help="Provider to set as default for all tiers.")],
    model: Annotated[str | None, typer.Option(help="Override the model id for all tiers (optional).", show_default=False)] = None,
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Set the default provider (and optionally model) for all tiers (fast, balanced, deep)."""
    profile = get_provider(provider)
    if profile is None:
        console.print(f"[red]Unknown provider:[/red] {provider}")
        raise typer.Exit(code=1)
    target, settings = _resolve_config(config)
    # Set all canonical tiers to this provider
    for tier in ("fast", "balanced", "deep"):
        settings.tier_policy[tier] = provider
        if model:
            current = settings.providers.get(provider) or ProviderOverride()
            models = dict(current.models_by_tier or {})
            models[tier] = model
            current.models_by_tier = models
            settings.providers[provider] = current
    _save_config(target, settings)
    msg = f"[green]✓[/green] Default provider for all tiers set to {provider}"
    if model:
        msg += f" (model={model})"
    console.print(msg)


def _resolve_config(config_path: Path | None) -> tuple[Path, AssAdeConfig]:
    target = config_path or default_config_path()
    return target, load_config(target)


def _save_config(path: Path, cfg: AssAdeConfig) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Persist without nexus_api_key — matches write_default_config behavior
    payload = cfg.model_dump(exclude={"nexus_api_key"})
    # Strip api_keys from per-provider overrides too (secrets don't go to disk)
    if "providers" in payload:
        for entry in payload["providers"].values():
            if isinstance(entry, dict):
                entry.pop("api_key", None)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────────────────────


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


def providers_test(
    name: Annotated[str, typer.Argument(help="Provider to ping (e.g., groq). Use 'all' to test every available one.")] = "all",
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Send a minimal request to verify the provider responds."""
    _, settings = _resolve_config(config)
    config_providers = {
        n: override.model_dump() for n, override in settings.providers.items()
    }

    names = [name] if name != "all" else [p.name for p in detect_available_providers(config_providers)]
    if not names:
        console.print("[yellow]No providers available to test.[/yellow]")
        raise typer.Exit(code=0)

    results = []
    for pname in names:
        profile = get_provider(pname)
        if profile is None:
            console.print(f"[red]Unknown provider:[/red] {pname}")
            continue
        user_override = settings.providers.get(pname)
        user_key = user_override.api_key if user_override else None
        api_key = profile.resolve_api_key(user_key) or ""
        base_url = (user_override.base_url if user_override and user_override.base_url else profile.base_url)
        if not base_url:
            results.append((pname, "skipped (no base_url)"))
            continue
        model = profile.model_for_tier(
            "fast",
            override=user_override.models_by_tier if user_override else None,
        ) or "default"
        try:
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            with httpx.Client(base_url=base_url.rstrip("/"), headers=headers, timeout=15.0) as client:
                resp = client.post(
                    "/chat/completions",
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": "Say 'ok' in one word."}],
                        "max_tokens": 8,
                        "temperature": 0.0,
                    },
                )
            if resp.status_code == 200:
                text = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "") or ""
                results.append((pname, f"[green]✓ {resp.status_code}[/green] — {text.strip()[:32]}"))
            else:
                err = resp.text[:120].replace("\n", " ")
                results.append((pname, f"[yellow]{resp.status_code}[/yellow] {err}"))
        except httpx.HTTPError as exc:
            results.append((pname, f"[red]error[/red] — {type(exc).__name__}: {str(exc)[:80]}"))

    table = Table(title="Provider connectivity test")
    table.add_column("Provider")
    table.add_column("Result")
    for pname, result in results:
        table.add_row(pname, result)
    console.print(table)


def providers_enable(
    name: Annotated[str, typer.Argument(help="Provider name to enable.")],
    config: Path | None = CONFIG_OPTION,  # noqa: ARG002
) -> None:
    """Enable a provider (include it in the fallback chain)."""
    _set_enabled(name, True, config)


def providers_disable(
    name: Annotated[str, typer.Argument(help="Provider name to disable.")],
    config: Path | None = CONFIG_OPTION,  # noqa: ARG002
) -> None:
    """Disable a provider (exclude from the fallback chain)."""
    _set_enabled(name, False, config)


def _set_enabled(name: str, enabled: bool, config: Path | None) -> None:
    if get_provider(name) is None:
        console.print(f"[red]Unknown provider:[/red] {name}")
        raise typer.Exit(code=1)
    target, settings = _resolve_config(config)
    current = settings.providers.get(name) or ProviderOverride()
    current.enabled = enabled
    settings.providers[name] = current
    _save_config(target, settings)
    status = "[green]enabled[/green]" if enabled else "[red]disabled[/red]"
    console.print(f"{name} → {status}")


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


def providers_set_key(
    provider: Annotated[str, typer.Argument(help="Provider name to set the API key for.")],
    api_key: Annotated[str, typer.Argument(help="API key value. NOT written to disk; session only.")],
) -> None:
    """Set a provider API key for this shell session (not persisted).

    For persistent keys, set the provider's env var in your .env file.
    Running `ass-ade providers env` prints the env vars per provider.
    """
    profile = get_provider(provider)
    if profile is None:
        console.print(f"[red]Unknown provider:[/red] {provider}")
        raise typer.Exit(code=1)
    if not profile.api_key_env:
        console.print(f"[yellow]{provider} doesn't use an API key.[/yellow]")
        raise typer.Exit(code=0)
    os.environ[profile.api_key_env] = api_key
    console.print(
        f"[green]✓[/green] {profile.api_key_env} set for this session.\n"
        f"[dim]To persist, add [bold]{profile.api_key_env}=...[/bold] to your .env file.[/dim]"
    )


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


def providers_env(
    # config argument removed as it was unused
) -> None:
    """Print env-var hints + signup URLs for every provider."""
    table = Table(title="Provider env vars")
    table.add_column("Provider", style="bold")
    table.add_column("Env var")
    table.add_column("Set?")
    table.add_column("Signup")

    for profile in FREE_PROVIDERS.values():
        env_name = profile.api_key_env or "(no key)"
        set_status = "[green]✓[/green]" if (profile.api_key_env and os.getenv(profile.api_key_env)) else "[dim]—[/dim]"
        if profile.local:
            set_status = "[yellow]local[/yellow]"
        signup = profile.signup_url or ""
        table.add_row(profile.display_name, env_name, set_status, signup)
    console.print(table)
    console.print("\n[dim]Add any of these to your .env file at the project root.[/dim]")
