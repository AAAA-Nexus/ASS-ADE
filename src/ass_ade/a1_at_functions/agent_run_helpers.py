"""Tier a1 — assimilated function 'agent_run'

Assimilated from: agent.py:151-205
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console

from ass_ade.config import default_config_path, load_config


# --- assimilated symbol ---
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

