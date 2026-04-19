# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/commands/agent.py:41
# Component id: at.source.ass_ade.agent_chat
__version__ = "0.1.0"

def agent_chat(
    config: Path | None = CONFIG_OPTION,
    working_dir: Annotated[Path, typer.Option(help="Working directory for the agent.")] = Path("."),
    model: Annotated[str | None, typer.Option(help="Specific model to use.")] = None,
) -> None:
    """Interactive agent chat session."""
    from ass_ade.agent.loop import AgentLoop
    from ass_ade.agent.gates import QualityGates
    from ass_ade.agent.lse import LSEEngine
    from ass_ade.agent.orchestrator import EngineOrchestrator
    from ass_ade.engine.router import build_provider
    from ass_ade.tools.registry import default_registry
    from ass_ade.nexus.client import NexusClient

    _, settings = _resolve_config(config)
    provider = build_provider(settings)
    registry = default_registry(str(working_dir.resolve()))

    gates_client = None
    try:
        gates = None
        nexus_for_engines = None
        if settings.profile in {"hybrid", "premium"} and settings.nexus_api_key:
            gates_client = NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
                agent_id=settings.agent_id,  # auto-deduct Nexus credit
            )
            gates = QualityGates(gates_client)
            nexus_for_engines = gates_client

        lse_cfg = _lse_config_from_settings(settings)
        lse = LSEEngine(lse_cfg)
        orchestrator = EngineOrchestrator(lse_cfg, nexus=nexus_for_engines, working_dir=str(working_dir.resolve()))

        agent = AgentLoop(
            provider=provider,
            registry=registry,
            working_dir=str(working_dir.resolve()),
            model=model or settings.agent_model,
            quality_gates=gates,
            orchestrator=orchestrator,
            lse=lse,
        )

        msg = f"[bold green]ASS-ADE Agent Ready[/bold green] (Model: {model or settings.agent_model} | Profile: {settings.profile})"
        console.print(msg)
        console.print("[dim]Type 'exit' or 'quit' to end the session.[/dim]\n")

        while True:
            try:
                line = console.input("[bold blue]user[/bold blue]> ").strip()
                if line.lower() in {"exit", "quit"}:
                    break
                if not line:
                    continue

                with console.status("[bold yellow]thinking...[/bold yellow]"):
                    response = agent.step(line)

                console.print(f"\n[bold magenta]assistant[/bold magenta]> {response}\n")
                _render_phase1_header(agent)

            except EOFError:
                break
            except KeyboardInterrupt:
                console.print("\n[yellow]Session interrupted.[/yellow]")
                break
            except Exception as exc:
                console.print(f"[bold red]Error:[/bold red] {exc}")
    finally:
        if gates_client:
            gates_client.close()
