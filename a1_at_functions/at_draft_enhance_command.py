# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_enhance_command.py:7
# Component id: at.source.a1_at_functions.enhance_command
from __future__ import annotations

__version__ = "0.1.0"

def enhance_command(
    path: Path = typer.Argument(Path("."), help="Folder to scan for enhancement opportunities."),
    config: Path | None = CONFIG_OPTION,
    apply: str | None = typer.Option(
        None,
        help="Comma-separated list of finding IDs to apply (e.g. --apply 1,3,5).",
    ),
    local_only: bool = typer.Option(
        False,
        help="Skip Nexus API; run local scanner and show findings only.",
    ),
    allow_remote: bool = typer.Option(
        False,
        help="Force remote enrichment even in local profile.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Print results as JSON."),
    limit: int = typer.Option(20, help="Maximum findings to display."),
) -> None:
    """Proactive enhancement recommendation cycle for any codebase.

    Scans for dead code, missing tests, security gaps, outdated patterns,
    long functions, bare excepts, missing docs, and TODO/FIXME markers.
    Rankings by impact and effort. Each applied recommendation auto-generates
    an AAAA-SPEC-004 blueprint and runs through rebuild -> validate -> certify.

    Pricing: $0.04/scan + $0.08/applied blueprint (free tier: 3 scans/day).
    Every result feeds the LoRA flywheel and earns Nexus API credits.

    Examples:
        ass-ade enhance .                          # scan and show findings
        ass-ade enhance . --allow-remote           # deep scan via Nexus
        ass-ade enhance . --apply 1,3,5            # apply selected fixes
        ass-ade enhance . --local-only --json      # local findings as JSON
    """
    from ass_ade.local.enhancer import build_enhancement_report
    from rich.table import Table as _Table

    _, settings = _resolve_config(config)
    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    # Check for NEXT_ENHANCEMENT.md planted by last rebuild
    next_enh_path = target / "NEXT_ENHANCEMENT.md"
    _prior_suggestions: list[str] = []
    if next_enh_path.exists():
        import re as _re
        text = next_enh_path.read_text(encoding="utf-8")
        # Extract numbered suggestion headings (### N. ...)
        _prior_suggestions = _re.findall(r"^###\s+\d+\.\s+(.+)$", text, _re.MULTILINE)
        if _prior_suggestions:
            console.print(
                f"\n[bold cyan]Found {len(_prior_suggestions)} enhancement suggestion(s) from last rebuild "
                f"([dim]{next_enh_path.name}[/dim]):[/bold cyan]"
            )
            for i, s in enumerate(_prior_suggestions, 1):
                console.print(f"  [cyan]{i}.[/cyan] {s}")
            console.print()

    console.print(f"[bold]Scanning[/bold] {target} for enhancement opportunities…")
    report = build_enhancement_report(target)
    total = report.get("total_findings", 0)
    by_impact = report.get("by_impact", {})
    console.print(
        f"[dim]Local scan: {report.get('scanned_files', 0)} files, "
        f"[red]{by_impact.get('high', 0)} high[/red] / "
        f"[yellow]{by_impact.get('medium', 0)} medium[/yellow] / "
        f"{by_impact.get('low', 0)} low impact findings[/dim]"
    )

    nexus_result: dict = {}
    use_remote = not local_only and _should_probe_remote(settings, allow_remote if allow_remote else None)

    if use_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                api_key=getattr(settings, "api_key", None),
                agent_id=str(settings.agent_id) if settings.agent_id else None,
                timeout=60.0,
            ) as nx:
                console.print("[dim]Deep scan via AAAA-Nexus enhancement engine…[/dim]")
                result = nx.enhance_scan(
                    local_report=report,
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                )
                nexus_result = result.model_dump()
                if result.ok and result.findings:
                    report["findings"] = result.findings
                    report["total_findings"] = result.total_findings
                    total = result.total_findings
                    console.print(
                        f"[green][OK][/green] Nexus deep scan: "
                        f"{result.total_findings} findings, "
                        f"{result.blueprints_generated} blueprints pre-generated"
                    )
                    if result.lora_captured:
                        console.print("[dim]LoRA flywheel: sample captured.[/dim]")
                    if result.credit_used:
                        console.print(f"[dim]Scan cost: ${result.credit_used:.4f}[/dim]")
        except Exception as exc:
            console.print(f"[yellow]Nexus scan unavailable:[/yellow] {exc}")
            console.print("[dim]Showing local findings only.[/dim]")

    findings = report.get("findings", [])[:limit]

    if json_out:
        _print_json({**report, "nexus_enriched": bool(nexus_result.get("ok"))})
        return

    if not findings:
        console.print("\n[green]No improvement opportunities found.[/green] Codebase looks clean.")
        return

    # Display findings table
    t = _Table(title=f"Enhancement Opportunities ({total} total, showing {len(findings)})")
    t.add_column("ID", style="bold", width=4)
    t.add_column("Impact", width=8)
    t.add_column("Effort", width=8)
    t.add_column("Category", width=18)
    t.add_column("Title")
    t.add_column("File", style="dim")

    impact_colors = {"high": "red", "medium": "yellow", "low": "green"}
    for f in findings:
        impact = f.get("impact", "low")
        color = impact_colors.get(impact, "white")
        line = f.get("line")
        loc = f.get("file", "")
        if line:
            loc = f"{loc}:{line}"
        t.add_row(
            str(f.get("id", "")),
            f"[{color}]{impact}[/{color}]",
            f.get("effort", ""),
            f.get("category", ""),
            f.get("title", ""),
            loc,
        )
    console.print(t)

    # Handle --apply
    if apply:
        try:
            ids = [int(x.strip()) for x in apply.split(",") if x.strip()]
        except ValueError:
            console.print("[red]--apply requires comma-separated integers (e.g. --apply 1,3,5)[/red]")
            raise typer.Exit(code=1)

        if not ids:
            console.print("[yellow]No valid IDs in --apply list.[/yellow]")
            raise typer.Exit(code=1)

        console.print(f"\n[bold]Applying findings[/bold] {ids}…")

        apply_result: dict = {}
        if use_remote:
            try:
                with NexusClient(
                    base_url=settings.nexus_base_url,
                    api_key=getattr(settings, "api_key", None),
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                    timeout=120.0,
                ) as nx:
                    res = nx.enhance_apply(
                        improvement_ids=ids,
                        local_report=report,
                        agent_id=str(settings.agent_id) if settings.agent_id else None,
                    )
                    apply_result = res.model_dump()
                    if res.ok:
                        console.print(
                            f"[green][OK][/green] Applied {res.applied_count} enhancements, "
                            f"{len(res.blueprints)} blueprints generated"
                        )
                        for bp in res.blueprints:
                            bp_id = bp.get("blueprint_id", bp.get("id", "?"))
                            bp_file = bp.get("file", f"blueprints/blueprint_{bp_id}.json")
                            bp_path = target / bp_file
                            import json as _json
                            bp_path.parent.mkdir(parents=True, exist_ok=True)
                            bp_path.write_text(_json.dumps(bp, indent=2), encoding="utf-8")
                            console.print(f"  [green]✓[/green] {bp_path}")
                        if res.lora_captured:
                            console.print("[dim]LoRA flywheel: sample captured.[/dim]")
                        if res.credit_used:
                            console.print(f"[dim]Apply cost: ${res.credit_used:.4f}[/dim]")
            except Exception as exc:
                console.print(f"[yellow]Nexus apply unavailable:[/yellow] {exc}")
        else:
            # Local-only: generate minimal draft blueprints
            selected = [f for f in report.get("findings", []) if f.get("id") in ids]
            import json as _json
            import datetime as _dt
            for finding in selected:
                slug = "".join(
                    c if c.isalnum() else "_"
                    for c in finding.get("title", "fix").lower()
                )[:40].strip("_")
                bp = {
                    "blueprint_schema": "AAAA-SPEC-004",
                    "id": f"bp.enhance.{slug}",
                    "name": finding.get("title", "Enhancement"),
                    "description": finding.get("description", ""),
                    "version": "1.0.0",
                    "status": "draft",
                    "source": "local-enhance",
                    "finding_id": finding.get("id"),
                    "category": finding.get("category"),
                    "target_file": finding.get("file"),
                    "created_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
                }
                _bp_dir = target / "blueprints"
                _bp_dir.mkdir(exist_ok=True)
                bp_path = _bp_dir / f"blueprint_{slug}.json"
                bp_path.write_text(_json.dumps(bp, indent=2), encoding="utf-8")
                console.print(f"  [green]✓[/green] Draft blueprint: {bp_path}")

        console.print(
            "\n[dim]Next: run [bold]ass-ade rebuild .[/bold] "
            "to materialize the blueprints.[/dim]"
        )
    else:
        console.print(
            f"\n[dim]Apply selected findings with: "
            f"[bold]ass-ade enhance . --apply 1,2,3[/bold][/dim]"
        )
