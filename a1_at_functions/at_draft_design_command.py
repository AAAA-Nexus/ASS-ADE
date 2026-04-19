# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_design_command.py:5
# Component id: at.source.ass_ade.design_command
__version__ = "0.1.0"

def design_command(
    description: Annotated[str, typer.Argument(help="Natural language description of what to build or enhance.")] = "",
    path: Path = typer.Option(Path("."), help="Target repository to design for."),
    config: Path | None = CONFIG_OPTION,
    out: Path | None = typer.Option(None, help="Write blueprint JSON to this file (default: blueprint_<slug>.json)."),
    parallel: Path | None = typer.Option(None, help="File with one description per line — generate all blueprints in sequence."),
    local_only: bool = typer.Option(False, help="Return a minimal local-only blueprint without API synthesis."),
    allow_remote: bool = typer.Option(False, help="Force remote API call even in local profile."),
    json_out: bool = typer.Option(False, "--json", help="Print blueprint as JSON."),
) -> None:
    """Blueprint engine: turn ideas into AAAA-SPEC-004 component blueprints.

    Takes a natural language description and produces a blueprint JSON file
    ready to feed into `ass-ade rebuild` for materialization.

    The monadic tier system guarantees no conflicts between parallel blueprints:
    each blueprint targets specific tiers and the composition law prevents
    collisions at the qk -> at -> mo -> og -> sy boundary.

    Free tier: 3 calls/day. Paid: x402 USDC or API key. Every result captured
    by the LoRA flywheel.

    Examples:
        ass-ade design "add OAuth2 login"
        ass-ade design "add OAuth2 login" --path ~/myproject --allow-remote
        ass-ade design "add caching layer" --out blueprint_cache.json
        ass-ade design --parallel descriptions.txt --allow-remote
    """
    import json as _json
    from ass_ade.local.docs_engine import build_local_analysis

    _, settings = _resolve_config(config)
    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    def _make_slug(text: str) -> str:
        return "".join(c if c.isalnum() else "_" for c in text.lower())[:40].strip("_")

    def _make_local_blueprint(desc: str, analysis: dict) -> dict:
        return {
            "schema": "AAAA-SPEC-004",
            "description": desc,
            "tiers": ["at", "mo"],
            "components": [],
            "status": "draft",
            "source": "local",
            "repo": analysis.get("metadata", {}).get("name", str(target)),
            "languages": list(analysis.get("languages", {}).keys()),
        }

    def _run_single(desc: str, out_path: Path | None, analysis: dict) -> dict:
        slug = _make_slug(desc)
        _blueprints_dir = Path("blueprints")
        _blueprints_dir.mkdir(exist_ok=True)
        resolved_out = out_path or _blueprints_dir / f"blueprint_{slug}.json"

        use_remote = not local_only and _should_probe_remote(settings, allow_remote if allow_remote else None)
        blueprint_dict: dict = {}
        result_meta: dict = {}

        if local_only or not use_remote:
            blueprint_dict = _make_local_blueprint(desc, analysis)
            console.print("[dim]Local blueprint generated (no API call).[/dim]")
        else:
            try:
                with NexusClient(
                    base_url=settings.nexus_base_url,
                    api_key=getattr(settings, "api_key", None),
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                    timeout=60.0,
                ) as nx:
                    console.print("[dim]Sending to atomadic.tech/v1/uep/design…[/dim]")
                    result = nx.design_blueprint(
                        description=desc,
                        context=analysis,
                        agent_id=str(settings.agent_id) if settings.agent_id else None,
                    )
                    result_meta = result.model_dump()
                    if result.ok and result.blueprint:
                        blueprint_dict = result.blueprint
                        console.print(
                            f"[green][OK][/green] Blueprint synthesized "
                            f"(id={result.blueprint_id}, "
                            f"tiers={result.target_tiers}, "
                            f"components={result.component_count})"
                        )
                        if result.lora_captured:
                            console.print("[dim]LoRA flywheel: sample captured.[/dim]")
                        if result.credit_used:
                            console.print(f"[dim]Credit used: ${result.credit_used:.6f}[/dim]")
                    else:
                        console.print(f"[yellow]Remote returned empty blueprint:[/yellow] {result.message}")
                        blueprint_dict = _make_local_blueprint(desc, analysis)
                        console.print("[dim]Falling back to local draft.[/dim]")
            except Exception as exc:
                console.print(f"[yellow]Remote synthesis unavailable:[/yellow] {exc}")
                blueprint_dict = _make_local_blueprint(desc, analysis)
                console.print("[dim]Falling back to local draft blueprint.[/dim]")

        resolved_out.write_text(_json.dumps(blueprint_dict, indent=2, default=str), encoding="utf-8")
        console.print(f"[green][OK][/green] Blueprint written: {resolved_out}")
        return {"description": desc, "file": str(resolved_out), "meta": result_meta}

    if parallel:
        if not parallel.exists():
            console.print(f"[red]Parallel file does not exist:[/red] {parallel}")
            raise typer.Exit(code=1)
        lines = [
            line.strip()
            for line in parallel.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if not lines:
            console.print("[yellow]No descriptions found in parallel file.[/yellow]")
            raise typer.Exit(code=1)

        console.print(f"[bold]Analyzing[/bold] {target}")
        analysis = build_local_analysis(target)
        results = []
        for i, desc in enumerate(lines, 1):
            console.print(f"\n[bold][{i}/{len(lines)}][/bold] {desc[:60]}")
            slug = _make_slug(desc)
            item_out = Path("blueprints") / f"blueprint_{i:02d}_{slug}.json"
            r = _run_single(desc, item_out, analysis)
            results.append(r)

        t = Table(title="Parallel Blueprint Summary")
        t.add_column("#", style="dim")
        t.add_column("Description")
        t.add_column("File")
        for i, r in enumerate(results, 1):
            t.add_row(str(i), r["description"][:50], r["file"])
        console.print()
        console.print(t)
        console.print(f"\n[green][OK][/green] {len(results)} blueprints generated.")
        if json_out:
            _print_json(results)
        return

    if not description:
        console.print("[red]A description argument is required (or use --parallel).[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]Designing[/bold] {description[:60]!r} for {target}")
    analysis = build_local_analysis(target)
    meta = analysis.get("metadata", {})
    console.print(
        f"[dim]Repo: {meta.get('name', 'unknown')} "
        f"({', '.join(list(analysis.get('languages', {}).keys())[:3])}), "
        f"{analysis.get('summary', {}).get('total_files', 0)} files[/dim]"
    )

    r = _run_single(description, out, analysis)

    if json_out:
        blueprint_data = _json.loads(Path(r["file"]).read_text(encoding="utf-8"))
        _print_json(blueprint_data)
