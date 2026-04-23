"""CLI sub-command: ``ass-ade feature`` — propose a blueprint for a new feature."""

from __future__ import annotations

import json
import os
from pathlib import Path

import typer
from rich.console import Console

from ass_ade.engine.rebuild.feature import propose_feature_blueprint

feature_app = typer.Typer(
    help="Propose a blueprint for a new feature. Build it with `ass-ade blueprint build`."
)
_console = Console()


@feature_app.command("propose")
def propose(
    description: str = typer.Argument(..., help="Feature description."),
    name: str = typer.Option(None, "--name", help="Short feature name (slug)."),
    target: Path = typer.Option(None, "--target", help="Target codebase for context."),
    out: Path = typer.Option(
        Path("./blueprints"), "--out", help="Output directory for the blueprint."
    ),
    nexus_url: str = typer.Option(None, help="Override AAAA-Nexus base URL."),
    allow_fallback: bool = typer.Option(
        False,
        "--allow-fallback",
        help="Permit a placeholder component when Nexus is unreachable. Non-production.",
    ),
) -> None:
    """Decompose ``description`` into tier-aligned components and emit an AAAA-SPEC-004 blueprint."""
    try:
        resolved_url = nexus_url or os.environ.get("AAAA_NEXUS_BASE_URL")
        kwargs: dict[str, object] = {}
        if resolved_url:
            kwargs["base_url"] = resolved_url
        blueprint = propose_feature_blueprint(
            description,
            feature_name=name,
            target=target.resolve() if target else None,
            api_key=os.environ.get("AAAA_NEXUS_API_KEY"),
            agent_id=os.environ.get("AAAA_NEXUS_AGENT_ID"),
            allow_fallback=allow_fallback,
            **kwargs,  # type: ignore[arg-type]
        )
    except RuntimeError as exc:
        _console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=2) from exc

    out.mkdir(parents=True, exist_ok=True)
    bp_path = out / f"{blueprint['blueprint_id']}.json"
    bp_path.write_text(json.dumps(blueprint, indent=2), encoding="utf-8")
    source = blueprint.get("metadata", {}).get("source", "unknown")
    _console.print(f"[green]blueprint written[/green] ({source} source)")
    _console.print(f"  file:       {bp_path}")
    _console.print(f"  components: {len(blueprint['components'])}")
    _console.print(f"  tiers:      {blueprint['tiers']}")
    _console.print("")
    _console.print(f"Next: [cyan]ass-ade blueprint build {bp_path}[/cyan]")
