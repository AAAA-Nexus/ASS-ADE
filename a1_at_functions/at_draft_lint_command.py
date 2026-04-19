# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_lint_command.py:5
# Component id: at.source.ass_ade.lint_command
__version__ = "0.1.0"

def lint_command(
    path: Path = typer.Argument(Path("."), help="Folder to lint."),
    config: Path | None = CONFIG_OPTION,
    fix: bool = typer.Option(False, help="Apply auto-fixes where supported (ruff --fix)."),
    local_only: bool = typer.Option(
        False,
        help="Skip Nexus synthesis; run local linters only.",
    ),
    allow_remote: bool = typer.Option(
        False,
        help="Force remote enrichment even in local profile.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
) -> None:
    """Run the monadic linter on any codebase.

    Detects and runs language-appropriate linters (ruff, pyright, eslint, clippy,
    go vet). Then sends findings to the AAAA-Nexus synthesis engine for intelligent
    gap analysis and remediation suggestions. Free tier: 3 calls/day. Paid: x402.

    Every lint run is captured by the LoRA flywheel.

    Examples:
        ass-ade lint .
        ass-ade lint ~/myproject --fix
        ass-ade lint ~/myproject --allow-remote --json
    """
    from ass_ade.local.linter import run_linters

    _, settings = _resolve_config(config)
    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Linting[/bold] {target}")
    lint_results = run_linters(target, fix=fix)

    for linter_name, res in lint_results.get("results", {}).items():
        ok_str = "[green]OK[/green]" if res.get("ok") else "[red]FAIL[/red]"
        count = res.get("error_count", 0) + res.get("warning_count", 0)
        console.print(f"  {linter_name}: [{ok_str}] {count} findings")

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
                console.print("[dim]Sending to AAAA-Nexus lint synthesis engine…[/dim]")
                result = nx.lint_analyze(
                    path_analysis=lint_results,
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                )
                nexus_result = result.model_dump()
                if result.ok:
                    console.print(f"[green][OK][/green] Nexus analysis: {result.findings_count} findings")
                    if result.lora_captured:
                        console.print("[dim]LoRA flywheel: sample captured.[/dim]")
        except Exception as exc:
            _http_status = (
                getattr(exc, "status_code", None)
                or getattr(getattr(exc, "response", None), "status_code", None)
            )
            if _http_status == 402:
                console.print("[yellow]Nexus synthesis unavailable — API credits required[/yellow]")
            else:
                console.print(f"[yellow]Nexus synthesis unavailable:[/yellow] {exc}")

    total = lint_results.get("total_findings", 0)
    payload = {
        **lint_results,
        "nexus_enriched": nexus_result.get("synthesis_applied", False),
        "lora_captured": nexus_result.get("lora_captured", False),
    }

    if json_out:
        _print_json(payload)
        return

    status = "[green]PASS[/green]" if total == 0 else f"[red]FAIL[/red] ({total} findings)"
    console.print(f"\n[bold]Lint result:[/bold] {status}")
    if total > 0:
        raise typer.Exit(code=1)
