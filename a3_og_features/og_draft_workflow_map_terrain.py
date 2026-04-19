# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/commands/workflow.py:211
# Component id: og.source.ass_ade.workflow_map_terrain
__version__ = "0.1.0"

def workflow_map_terrain(
    task_description: str = typer.Argument(..., help="Task to validate before execution."),
    agent: list[str] = typer.Option([], "--agent", help="Required agent capability."),
    hook: list[str] = typer.Option([], "--hook", help="Required hook capability."),
    skill: list[str] = typer.Option([], "--skill", help="Required skill capability."),
    tool: list[str] = typer.Option([], "--tool", help="Required tool capability."),
    harness: list[str] = typer.Option([], "--harness", help="Required harness capability."),
    requirements_file: Path | None = typer.Option(None, help="JSON file with grouped required_capabilities."),
    auto_invent: bool = typer.Option(False, "--auto-invent", help="Persist development-plan assets for eligible Tool/Skill gaps."),
    max_budget: float = typer.Option(1.0, help="Maximum development budget in USDC."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """MAP = TERRAIN gate: halt and invent when required capabilities are missing."""
    from ass_ade.map_terrain import map_terrain

    _, settings = _resolve_config(config)
    required: dict[str, list[str]] = {
        "agents": list(agent),
        "hooks": list(hook),
        "skills": list(skill),
        "tools": list(tool),
        "harnesses": list(harness),
    }
    if requirements_file is not None:
        try:
            loaded = json.loads(requirements_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"[red]Failed to read requirements:[/red] {exc}")
            raise typer.Exit(code=4) from exc
        if isinstance(loaded, dict) and "required_capabilities" in loaded:
            loaded = loaded["required_capabilities"]
        if not isinstance(loaded, dict):
            console.print("[red]Requirements file must contain an object.[/red]")
            raise typer.Exit(code=4)
        for key, value in loaded.items():
            if isinstance(value, list):
                required[key] = [str(item) for item in value]

    hosted_tools: list[str] = []
    if settings.profile != "local" or allow_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
            ) as client:
                manifest = client.get_mcp_manifest()
            hosted_tools = [item.name or "" for item in manifest.tools]
        except httpx.HTTPError:
            hosted_tools = []

    result = map_terrain(
        task_description=task_description,
        required_capabilities=required,
        agent_id=settings.agent_id,
        max_development_budget_usdc=max_budget,
        auto_invent_if_missing=auto_invent,
        working_dir=Path("."),
        hosted_tools=hosted_tools,
    )

    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    color = "green" if result.verdict == "PROCEED" else "yellow"
    console.print(f"[{color}]MAP = TERRAIN: {result.verdict}[/{color}]")
    if result.missing_capabilities:
        console.print("[bold]Missing capabilities:[/bold]")
        for item in result.missing_capabilities:
            console.print(f"  - {item.type}: {item.name} via {item.recommended_creation_tool}")
    console.print(f"Next: {result.next_action}")
    if result.development_plan and result.development_plan.created_assets:
        console.print("[bold]Created development-plan assets:[/bold]")
        for path in result.development_plan.created_assets:
            console.print(f"  - {path}")
