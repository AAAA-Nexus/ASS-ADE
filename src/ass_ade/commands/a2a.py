"""A2A Interop command group — agent card validation, negotiation, and discovery."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer
from rich.console import Console

from ass_ade.a2a import fetch_agent_card, local_agent_card, negotiate
from ass_ade.config import default_config_path, load_config
from ass_ade.nexus.client import NexusClient

console = Console()

CONFIG_OPTION = typer.Option(None, help="Path to the ASS-ADE config file.")
ALLOW_REMOTE_OPTION = typer.Option(
    False, help="Permit remote calls when profile is local."
)


def _resolve_config(config_path: Path | None) -> tuple[Path, Any]:
    target = config_path or default_config_path()
    return target, load_config(target)


def _require_remote_access(settings: Any, allow_remote: bool) -> None:
    if settings.profile == "local" and not allow_remote:
        console.print(
            "Remote AAAA-Nexus calls are disabled in the local profile. "
            "Use --allow-remote or switch the profile to hybrid/premium."
        )
        raise typer.Exit(code=2)


def _nexus_err(exc: httpx.HTTPError) -> None:
    """Print a Nexus error message."""
    console.print(f"[red]Remote error:[/red] {exc}")


def register(app: typer.Typer) -> None:
    """Register A2A commands on the provided app."""
    app.command("validate")(a2a_validate)
    app.command("negotiate")(a2a_negotiate)
    app.command("discover")(a2a_discover)


def a2a_validate(
    agent_card_path: Annotated[Path, typer.Argument(help="Path to the card.")],
) -> None:
    """Validate an A2A agent card format and structure."""
    from ass_ade.a2a import validate_agent_card

    if not agent_card_path.exists():
        console.print(f"[red]Error:[/red] File not found: {agent_card_path}")
        raise typer.Exit(code=1)

    try:
        data = json.loads(agent_card_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        console.print(f"[red]Error:[/red] Failed to parse JSON: {exc}")
        raise typer.Exit(code=1) from exc

    # Use library validation
    report = validate_agent_card(data)

    # Display validation results
    if report.valid:
        console.print("[green]✓ Valid A2A Agent Card[/green]")
    else:
        console.print("[red]✗ Invalid A2A Agent Card[/red]")

    # Show errors
    if report.errors:
        console.print("\n[red]Errors:[/red]")
        for issue in report.errors:
            console.print(f"  • {issue.field}: {issue.message}")

    # Show warnings
    if report.warnings:
        console.print("\n[yellow]Warnings:[/yellow]")
        for issue in report.warnings:
            console.print(f"  • {issue.field}: {issue.message}")

    # Show parsed card
    if report.card:
        console.print("\n[bold]Card Details:[/bold]")
        console.print(json.dumps(report.card.model_dump(), indent=2), markup=False)

    # Exit with error code if validation failed
    if not report.valid:
        raise typer.Exit(code=1)


def a2a_negotiate(
    remote_url: Annotated[str, typer.Argument(help="Base URL of the remote agent to negotiate with.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Compare local ASS-ADE agent card with a remote agent for A2A interoperability."""
    from ass_ade.nexus.validation import validate_url

    _, settings = _resolve_config(config)

    try:
        validate_url(remote_url)
    except ValueError as exc:
        console.print(f"[red]Blocked:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    local = local_agent_card(str(Path(".").resolve()))
    report = fetch_agent_card(remote_url)
    if not report.valid or not report.card:
        msgs = [issue.message for issue in report.errors]
        console.print(f"[red]Remote agent card invalid:[/red] {msgs}")
        raise typer.Exit(code=1)

    result = negotiate(local, report.card)
    console.print(json.dumps({
        "compatible": result.compatible,
        "shared_skills": result.shared_skills,
        "local_only": result.local_only,
        "remote_only": result.remote_only,
        "auth_compatible": result.auth_compatible,
        "notes": result.notes,
    }, indent=2), markup=False)
    if not result.compatible:
        raise typer.Exit(code=1)


def a2a_discover(
    capability: Annotated[str, typer.Argument(help="Capability to search for.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Discover agents matching a capability."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            results = client.discovery_search(capability=capability)
            # Convert to JSON-serializable format
            if hasattr(results, 'model_dump'):
                results_dict = results.model_dump()
            else:
                results_dict = results
            console.print(json.dumps(results_dict, indent=2), markup=False)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
