"""Fix the a2a commands and pipeline_run function in cli.py."""

with open("src/ass_ade/cli.py", encoding="utf-8") as f:
    content = f.read()

# ── Fix 1: Replace OLD module-level a2a commands ──────────────────────────────

OLD_A2A = '''# ------------------------------------------------------------------------------
# A2A commands - validate, negotiate, discover
# ------------------------------------------------------------------------------

@a2a_app.command("validate")
def a2a_validate(
    agent_card_path: Annotated[Path, typer.Argument(help="Path to the card.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    from ass_ade.nexus.validation import validate_url

    if not agent_card_path.exists():
        console.print(f"[red]Error:[/red] File not found: {agent_card_path}")
        raise typer.Exit(code=1)

    try:
        data = json.loads(agent_card_path.read_text(encoding="utf-8"))
        required = {"name", "description", "capabilities", "endpoint"}
        missing = required - set(data.keys())
        if missing:
            console.print(f"[red]Invalid Card:[/red] Missing fields: {', '.join(missing)}")
            raise typer.Exit(code=1)

        validate_url(data["endpoint"])
        console.print("[green]A2A Agent Card is valid.[/green]")
        _print_json(data)

    except (json.JSONDecodeError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc


@a2a_app.command("negotiate")
def a2a_negotiate(
    target_agent_id: Annotated[str, typer.Argument(help="Agent ID to negotiate with.")],
    task_description: Annotated[str, typer.Argument(help="Task description.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    from ass_ade.nexus.validation import validate_agent_id

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    aid = validate_agent_id(target_agent_id)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            match = client.agent_capabilities_match(task=task_description)
            intent = client.agent_intent_classify(text=task_description)
            plan = client.agent_plan(goal=task_description)

            result = {
                "target_agent": aid,
                "task": task_description,
                "matches": match.model_dump() if hasattr(match, "model_dump") else match,
                "intent": intent.model_dump() if hasattr(intent, "model_dump") else intent,
                "proposed_plan": plan.model_dump() if hasattr(plan, "model_dump") else plan,
                "status": "negotiation_started"
            }
            console.print("[green]Negotiation initialized.[/green]")
            _print_json(result)

    except (httpx.HTTPError, ValueError) as exc:
        if isinstance(exc, httpx.HTTPError):
            _nexus_err(exc)
        else:
            console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(code=1) from exc


@a2a_app.command("discover")
def a2a_discover(
    capability: Annotated[str, typer.Argument(help="Capability to search for.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            results = client.discovery_search(capability=capability)
            _print_json(results)
    except httpx.HTTPError as exc:
        _nexus_err(exc)'''

NEW_A2A = '''# ------------------------------------------------------------------------------
# A2A commands - validate, negotiate, discover
# ------------------------------------------------------------------------------

@a2a_app.command("validate")
def a2a_validate(
    url: Annotated[str, typer.Argument(help="URL of the agent to validate.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Fetch and validate a remote A2A agent card."""
    from ass_ade.a2a import fetch_agent_card

    report = fetch_agent_card(url)
    if report.valid and report.card:
        console.print("[green]Valid[/green] A2A agent card.")
        _print_json(report.card.model_dump())
    else:
        for issue in report.issues:
            console.print(f"[red]{issue.severity}[/red] [{issue.field}] {issue.message}")
        raise typer.Exit(code=1)


@a2a_app.command("negotiate")
def a2a_negotiate(
    url: Annotated[str, typer.Argument(help="URL of the remote agent to negotiate with.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Negotiate capabilities with a remote A2A agent."""
    from ass_ade.a2a import fetch_agent_card, generate_local_card, negotiate_capabilities

    report = fetch_agent_card(url)
    if not report.valid or not report.card:
        for issue in report.issues:
            console.print(f"[red]{issue.severity}[/red] [{issue.field}] {issue.message}")
        raise typer.Exit(code=1)

    local = generate_local_card()
    result = negotiate_capabilities(local, report.card)
    _print_json({
        "compatible": result.compatible,
        "shared_skills": result.shared_skills,
        "local_only": result.local_only,
        "remote_only": result.remote_only,
        "auth_compatible": result.auth_compatible,
        "notes": result.notes,
    })


@a2a_app.command("discover")
def a2a_discover(
    url: Annotated[str, typer.Argument(help="URL of the agent to discover.")],
    json_output: bool = typer.Option(False, "--json", help="Output card as JSON."),
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Fetch and display an A2A agent card."""
    from ass_ade.a2a import fetch_agent_card

    report = fetch_agent_card(url)
    if not report.valid or not report.card:
        for issue in report.issues:
            console.print(f"[red]{issue.severity}[/red] [{issue.field}] {issue.message}")
        raise typer.Exit(code=1)

    if json_output:
        print(report.card.model_dump_json())
    else:
        card = report.card
        console.print(f"[bold]{card.name}[/bold] v{card.version}")
        if card.description:
            console.print(card.description)
        for skill in card.skills:
            console.print(f"  \u2022 {skill.name}: {skill.description}")'''

# ── Fix 2: Replace corrupt pipeline_run function ──────────────────────────────

OLD_PIPELINE_RUN = '''    def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
        color = "green" if status == StepStatus.PASSED else "red"
        @a2a_app.command("validate")
        def a2a_validate(
            url: Annotated[str, typer.Argument(help="URL of the agent to validate.")],
            config: Path | None = CONFIG_OPTION,
        ) -> None:
            """Fetch and validate a remote A2A agent card."""
            from ass_ade.a2a import fetch_agent_card

            report = fetch_agent_card(url)
            if report.valid and report.card:
                console.print("[green]Valid[/green] A2A agent card.")
                _print_json(report.card.model_dump())
            else:
                for issue in report.issues:
                    console.print(f"[red]{issue.severity}[/red] [{issue.field}] {issue.message}")
                raise typer.Exit(code=1)


        @a2a_app.command("negotiate")
        def a2a_negotiate(
            url: Annotated[str, typer.Argument(help="URL of the remote agent to negotiate with.")],
            config: Path | None = CONFIG_OPTION,
        ) -> None:
            """Negotiate capabilities with a remote A2A agent."""
            from ass_ade.a2a import fetch_agent_card, generate_local_card, negotiate_capabilities

            report = fetch_agent_card(url)
            if not report.valid or not report.card:
                for issue in report.issues:
                    console.print(f"[red]{issue.severity}[/red] [{issue.field}] {issue.message}")
                raise typer.Exit(code=1)

            local = generate_local_card()
            result = negotiate_capabilities(local, report.card)
            _print_json({
                "compatible": result.compatible,
                "shared_skills": result.shared_skills,
                "local_only": result.local_only,
                "remote_only": result.remote_only,
                "auth_compatible": result.auth_compatible,
                "notes": result.notes,
            })


        @a2a_app.command("discover")
        def a2a_discover(
            url: Annotated[str, typer.Argument(help="URL of the agent to discover.")],
            json_output: bool = typer.Option(False, "--json", help="Output card as JSON."),
            config: Path | None = CONFIG_OPTION,
        ) -> None:
            """Fetch and display an A2A agent card."""
            from ass_ade.a2a import fetch_agent_card

            report = fetch_agent_card(url)
            if not report.valid or not report.card:
                for issue in report.issues:
                    console.print(f"[red]{issue.severity}[/red] [{issue.field}] {issue.message}")
                raise typer.Exit(code=1)

            if json_output:
                import sys
                print(report.card.model_dump_json())
            else:
                card = report.card
                console.print(f"[bold]{card.name}[/bold] v{card.version}")
                if card.description:
                    console.print(card.description)
                for skill in card.skills:
                    console.print(f"  \u2022 {skill.name}: {skill.description}")
    agent_id: str = typer.Argument(..., help="Agent ID to create a session for."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write session JSON to this path."),
) -> None:
    """Register a new RatchetGate session. $0.008/call.

    Fixes MCP CVE-2025-6514 \u2014 credentials can\'t outlive their proof window.
    """
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            session = client.ratchet_register(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    data = session.model_dump()
    table = Table(title="RatchetGate Session")
    for k, v in data.items():
        if v is not None:
            table.add_row(k, str(v))
    console.print(table)
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(data, indent=2), encoding="utf-8")'''

NEW_PIPELINE_RUN = '''    def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
        color = "green" if status == StepStatus.PASSED else "red"
        if status == StepStatus.RUNNING:
            color = "yellow"
        console.print(f"[{current}/{total}] {name}: [{color}]{status.value}[/{color}]")'''

# Apply fixes
if OLD_A2A in content:
    content = content.replace(OLD_A2A, NEW_A2A, 1)
    print("✓ Fixed module-level a2a commands")
else:
    print("✗ Could not find OLD_A2A block")

if OLD_PIPELINE_RUN in content:
    content = content.replace(OLD_PIPELINE_RUN, NEW_PIPELINE_RUN, 1)
    print("✓ Fixed pipeline_run function")
else:
    print("✗ Could not find OLD_PIPELINE_RUN block")

with open("src/ass_ade/cli.py", "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
try:
    py_compile.compile("src/ass_ade/cli.py", doraise=True)
    print("✓ Syntax OK")
except py_compile.PyCompileError as e:
    print(f"✗ Syntax error: {e}")
    import re
    m = re.search(r'line (\d+)', str(e))
    if m:
        lineno = int(m.group(1))
        lines = content.splitlines()
        for i in range(max(0, lineno-3), min(len(lines), lineno+3)):
            print(f"  {i+1}: {lines[i]!r}")
