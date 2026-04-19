# Extracted from C:/!ass-ade/src/ass_ade/commands/providers.py:296
# Component id: at.source.ass_ade.providers_set_key
from __future__ import annotations

__version__ = "0.1.0"

def providers_set_key(
    provider: Annotated[str, typer.Argument(help="Provider name to set the API key for.")],
    api_key: Annotated[str, typer.Argument(help="API key value. NOT written to disk; session only.")],
    config: Path | None = CONFIG_OPTION,
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
