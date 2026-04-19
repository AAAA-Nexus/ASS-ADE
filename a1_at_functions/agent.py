"""Agent command group — agentic IDE surface for chat and task execution."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console

from ass_ade.config import default_config_path, load_config

console = Console()

CONFIG_OPTION = typer.Option(None, help="Path to the ASS-ADE config file.")


def _resolve_config(config_path: Path | None) -> tuple[Path, Any]:
    target = config_path or default_config_path()
    return target, load_config(target)


def _lse_config_from_settings(settings: Any) -> dict[str, Any]:
    """Convert AssAdeConfig provider/tier settings to the dict shape LSE expects."""
    providers: dict[str, dict[str, Any]] = {}
    for name, override in (getattr(settings, "providers", {}) or {}).items():
        providers[name] = override.model_dump() if hasattr(override, "model_dump") else dict(override)
    return {
        "tier_policy": dict(getattr(settings, "tier_policy", {}) or {}),
        "provider_fallback_chain": list(getattr(settings, "provider_fallback_chain", []) or []),
        "providers": providers,
    }


def register(app: typer.Typer) -> None:
    """Register agent commands on the provided app."""
    app.command("chat")(agent_chat)
    app.command("run")(agent_run)


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


def _render_phase1_header(agent: Any) -> None:
    """Surface Phase 1 telemetry: SAM TRS, LSE tier, D_MAX depth.

    Fail-safe: tolerates mock agents and missing engines by type-checking
    every field before rendering.
    """
    bits: list[str] = []
    try:
        sam = getattr(agent, "last_sam_result", None)
        if isinstance(sam, dict):
            composite = sam.get("composite", 0.0)
            g23 = sam.get("g23", True)
            if isinstance(composite, (int, float)):
                color = "green" if composite >= 0.7 else ("yellow" if composite >= 0.5 else "red")
                g23_mark = "✓" if g23 else "✗"
                bits.append(f"[{color}]TRS={composite:.2f}[/{color}] G23={g23_mark}")
        lse = getattr(agent, "last_lse_decision", None)
        lse_tier = getattr(lse, "tier", None) if lse is not None else None
        if isinstance(lse_tier, str):
            bits.append(f"[cyan]LSE={lse_tier}[/cyan]")
        depth = getattr(agent, "delegation_depth", None)
        if isinstance(depth, int) and depth > 0:
            bits.append(f"[dim]depth={depth}/23[/dim]")
        cycle = getattr(agent, "last_cycle_report", None)
        wisdom = getattr(cycle, "wisdom_score", None) if cycle is not None else None
        if isinstance(wisdom, (int, float)) and wisdom > 0:
            bits.append(f"[dim]wisdom={wisdom:.0%}[/dim]")
        if bits:
            console.print("[dim]└─[/dim] " + " · ".join(bits))
    except Exception:
        # Header rendering must never break a command flow
        pass


def agent_run(
    task: Annotated[str, typer.Argument(help="Task for the agent to execute.")],
    config: Path | None = CONFIG_OPTION,
    working_dir: Annotated[Path, typer.Option(help="Working directory for the agent.")] = Path("."),
    model: Annotated[str | None, typer.Option(help="Specific model to use.")] = None,
) -> None:
    """Execute a single task using the agent."""
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

        with console.status("[bold yellow]Executing task...[/bold yellow]"):
            response = agent.step(task)

        console.print(response)
        _render_phase1_header(agent)
    finally:
        if gates_client:
            gates_client.close()
