"""Tier a1 — assimilated function 'build_blueprint'

Assimilated from: blueprint.py:119-222
"""

from __future__ import annotations


# --- assimilated symbol ---
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
        from ass_ade.engine.registry import default_registry

        registry_snapshot = default_registry().snapshot()
    except Exception:
        registry_snapshot = None
    try:
        result = rebuild_project(
            source_path=sources if len(sources) > 1 else sources[0],
            output_dir=out,
            registry=registry_snapshot,
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

