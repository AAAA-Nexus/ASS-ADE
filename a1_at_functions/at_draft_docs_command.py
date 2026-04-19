# Extracted from C:/!ass-ade/src/ass_ade/cli.py:6068
# Component id: at.source.ass_ade.docs_command
from __future__ import annotations

__version__ = "0.1.0"

def docs_command(
    path: Path = typer.Argument(Path("."), help="Folder to generate documentation for."),
    config: Path | None = CONFIG_OPTION,
    output_dir: Path | None = typer.Option(None, help="Override output directory (default: <path>)."),
    local_only: bool = typer.Option(
        False,
        help="Skip Nexus API synthesis; generate docs from local analysis only.",
    ),
    allow_remote: bool = typer.Option(
        False,
        help="Force remote enrichment even in local profile.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
) -> None:
    """Auto-generate a full documentation suite for any repository.

    Performs local AST analysis (free, instant) then sends the analysis to the
    AAAA-Nexus docs synthesis engine for intelligent gap-filling and enrichment.
    Free tier: 3 calls/day. Paid: x402 USDC or API key.

    Generated files (written to <path> or --output-dir):
      README.md · ARCHITECTURE.md · FEATURES.md · USER_GUIDE.md
      .gitignore · CONTRIBUTING.md · CHANGELOG.md

    Every synthesis result is captured by the LoRA flywheel to improve
    future runs automatically.

    Examples:
        ass-ade docs .
        ass-ade docs ~/myproject --local-only
        ass-ade docs ~/myproject --allow-remote --json
    """
    from ass_ade.local.docs_engine import build_local_analysis, render_local_docs

    _, settings = _resolve_config(config)
    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    out = output_dir.resolve() if output_dir else target
    console.print(f"[bold]Analyzing[/bold] {target}")

    analysis = build_local_analysis(target)
    meta = analysis.get("metadata", {})
    console.print(
        f"[dim]Detected: {meta.get('name', 'unknown')} "
        f"({', '.join(list(analysis.get('languages', {}).keys())[:3])}), "
        f"{analysis.get('summary', {}).get('total_files', 0)} files[/dim]"
    )

    # Local doc generation (always runs)
    console.print(f"[dim]Generating local docs -> {out}[/dim]")
    written = render_local_docs(analysis, out)

    nexus_result: dict = {}
    use_remote = not local_only and _should_probe_remote(settings, allow_remote if allow_remote else None)

    if use_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                api_key=settings.nexus_api_key,
                agent_id=str(settings.agent_id) if settings.agent_id else None,
                timeout=60.0,
            ) as nx:
                console.print("[dim]Enriching via AAAA-Nexus synthesis engine…[/dim]")
                result = nx.docs_generate(
                    path_analysis=analysis,
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                )
                nexus_result = result.model_dump()
                if result.ok:
                    console.print(
                        f"[green][OK][/green] Nexus synthesis applied "
                        f"({result.files_generated or []} enriched)"
                    )
                    if result.lora_captured:
                        console.print("[dim]LoRA flywheel: sample captured.[/dim]")
                    if result.credit_used:
                        console.print(f"[dim]Credit used: ${result.credit_used:.6f}[/dim]")
        except Exception as exc:
            console.print(f"[yellow]Nexus synthesis unavailable:[/yellow] {exc}")
            console.print("[dim]Falling back to local-only output.[/dim]")

    payload = {
        "ok": True,
        "path": str(target),
        "output_dir": str(out),
        "files_generated": [p.name for p in written.values()],
        "nexus_enriched": nexus_result.get("synthesis_applied", False),
        "lora_captured": nexus_result.get("lora_captured", False),
    }

    if json_out:
        _print_json(payload)
        return

    console.print()
    for name, fpath in written.items():
        console.print(f"  [green]✓[/green] {fpath}")
    console.print(f"\n[green][OK][/green] {len(written)} docs written to {out}")
