"""Blueprint sub-command — build production-grade code from a blueprint.

Wires the existing rebuild orchestrator with strict-no-stubs synthesis so
``ass-ade blueprint build <spec>`` takes a blueprint JSON and emits a complete,
CIE-gated, certificate-backed package. No stubs, no TODOs.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from ass_ade.engine.rebuild.orchestrator import rebuild_project
from ass_ade.engine.rebuild.synthesis import SynthesisFailure

blueprint_app = typer.Typer(
    help="Blueprint → production-grade codebase (no stubs, certificate-backed)."
)
_console = Console()

_BLUEPRINT_REQUIRED_FIELDS = ("schema", "description")


def _resolve_blueprints_dir() -> Path:
    override = os.environ.get("ASS_ADE_BLUEPRINTS_DIR")
    if override:
        return Path(override).expanduser()
    cwd_bp = Path.cwd() / "blueprints"
    if cwd_bp.is_dir():
        return cwd_bp
    return Path.cwd()


def _load_blueprint(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise typer.BadParameter(f"Blueprint file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise typer.BadParameter(f"Blueprint must be a JSON object, got {type(data).__name__}")
    return data


def _validate_blueprint(data: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    for field in _BLUEPRINT_REQUIRED_FIELDS:
        if field not in data:
            problems.append(f"missing required field: {field}")
    schema = data.get("schema")
    if schema and not isinstance(schema, str):
        problems.append("schema must be a string")
    if schema and not schema.startswith("AAAA-SPEC-") and not schema.startswith("ASSADE-SPEC-"):
        problems.append(f"unrecognized schema: {schema!r}")
    if "components" in data and not isinstance(data["components"], list):
        problems.append("components must be a list")
    if "tiers" in data and not isinstance(data["tiers"], list):
        problems.append("tiers must be a list")
    return problems


@blueprint_app.command("list")
def list_blueprints(
    directory: Path = typer.Option(
        None,
        "--dir",
        "-d",
        help="Directory to scan. Defaults to $ASS_ADE_BLUEPRINTS_DIR or ./blueprints.",
    ),
) -> None:
    """List blueprint files found under the blueprints directory."""
    target = directory or _resolve_blueprints_dir()
    if not target.is_dir():
        _console.print(f"[yellow]no blueprints directory at {target}[/yellow]")
        raise typer.Exit(code=0)
    matches = sorted(target.glob("blueprint*.json"))
    if not matches:
        _console.print(f"[yellow]no blueprints in {target}[/yellow]")
        raise typer.Exit(code=0)
    table = Table(title=f"Blueprints in {target}")
    table.add_column("file", style="cyan")
    table.add_column("description")
    table.add_column("components", justify="right")
    for path in matches:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            table.add_row(path.name, "[red]invalid JSON[/red]", "-")
            continue
        desc = str(data.get("description", ""))[:60]
        comps = data.get("components") or []
        table.add_row(path.name, desc, str(len(comps)))
    _console.print(table)


@blueprint_app.command("validate")
def validate_blueprint(
    spec: Path = typer.Argument(..., help="Path to blueprint JSON."),
) -> None:
    """Validate a blueprint file against the minimum schema."""
    data = _load_blueprint(spec)
    problems = _validate_blueprint(data)
    if problems:
        _console.print(f"[red]invalid[/red] ({len(problems)} issue(s)):")
        for p in problems:
            _console.print(f"  - {p}")
        raise typer.Exit(code=1)
    _console.print(f"[green]valid[/green] ({data.get('schema', 'unknown schema')})")


@blueprint_app.command("build")
def build_blueprint(
    spec: Path = typer.Argument(..., help="Path to blueprint JSON."),
    source: list[Path] = typer.Option(
        None,
        "--source",
        "-s",
        help="Source directory to ingest. Repeatable. Defaults to cwd.",
    ),
    out: Path = typer.Option(
        Path("./.ass-ade/builds"),
        "--out",
        "-o",
        help="Output parent directory for the timestamped build folder.",
    ),
    max_synthesize: int = typer.Option(
        50, "--max-synthesize", help="Maximum components to synthesize."
    ),
    max_refine: int = typer.Option(
        3, "--max-refine", help="Maximum refinement attempts per component."
    ),
    allow_stubs: bool = typer.Option(
        False,
        "--allow-stubs",
        help="Permit deterministic stub fallback when Nexus is unreachable. Non-production.",
    ),
    nexus_base_url: str = typer.Option(
        None, "--nexus-url", help="Override AAAA-Nexus base URL."
    ),
) -> None:
    """Build a production-grade codebase from a blueprint (no stubs by default)."""
    data = _load_blueprint(spec)
    problems = _validate_blueprint(data)
    if problems:
        _console.print(f"[red]blueprint invalid:[/red] {problems}")
        raise typer.Exit(code=1)

    # ── Premium gate — blueprint build requires API key ───────────────────────
    from ass_ade.a0_qk_constants.auth_gate_types import PremiumFeature, TIER_MESSAGE
    from ass_ade.a3_og_features.auth_gate import PremiumGateError, log_usage, require_premium
    from ass_ade.config import load_config as _load_config
    _bp_settings = _load_config()
    try:
        _bp_premium_key = require_premium(
            PremiumFeature.BLUEPRINT_BUILD,
            base_url=_bp_settings.nexus_base_url,
            api_key=_bp_settings.nexus_api_key,
            agent_id=str(_bp_settings.agent_id) if _bp_settings.agent_id else None,
        )
    except PremiumGateError as exc:
        _console.print("\n[bold yellow]Premium feature — API key required[/bold yellow]\n")
        for _ln in str(exc).splitlines():
            _console.print(_ln)
        raise typer.Exit(code=2) from exc

    sources = [p.resolve() for p in (source or [Path.cwd()])]
    out.mkdir(parents=True, exist_ok=True)

    _console.print(f"[bold]ass-ade blueprint build[/bold] :: {spec.name}")
    _console.print(f"  sources: {[str(p) for p in sources]}")
    _console.print(f"  out:     {out}")
    _console.print(f"  strict:  no-stubs={not allow_stubs}")

    resolved_url = nexus_base_url or os.environ.get("AAAA_NEXUS_BASE_URL")
    kwargs: dict[str, object] = {}
    if resolved_url:
        kwargs["nexus_base_url"] = resolved_url
    try:
        result = rebuild_project(
            source_path=sources if len(sources) > 1 else sources[0],
            output_dir=out,
            synthesize_gaps=True,
            blueprints=[data],
            nexus_api_key=os.environ.get("AAAA_NEXUS_API_KEY"),
            nexus_agent_id=os.environ.get("AAAA_NEXUS_AGENT_ID"),
            max_synthesize=max_synthesize,
            **kwargs,  # type: ignore[arg-type]
        )
    except SynthesisFailure as exc:
        _console.print(f"[red]synthesis failed:[/red] {exc}")
        raise typer.Exit(code=2) from exc

    log_usage(
        PremiumFeature.BLUEPRINT_BUILD,
        base_url=_bp_settings.nexus_base_url,
        api_key=_bp_premium_key,
        agent_id=str(_bp_settings.agent_id) if _bp_settings.agent_id else None,
    )

    summary = (result or {}).get("summary") or {}
    synth = summary.get("synthesis") or {}
    cert_path = result.get("certificate_path") if isinstance(result, dict) else None
    _console.print("[green]build complete[/green]")
    _console.print(f"  synthesized: {synth.get('synthesized_count', 0)}")
    _console.print(f"  rejected:    {synth.get('rejected_count', 0)}")
    _console.print(f"  stubs:       {synth.get('stub_used', 0)}")
    if cert_path:
        _console.print(f"  certificate: {cert_path}")


def register_blueprint_app(parent: typer.Typer) -> None:
    """Attach the blueprint sub-app to a parent typer.

    Kept as a helper so integration tests and alternative CLI front-ends can
    mount the command without importing the top-level ``ass_ade.cli`` module.
    """
    parent.add_typer(blueprint_app, name="blueprint")
