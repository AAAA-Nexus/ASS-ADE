# Extracted from C:/!ass-ade/src/ass_ade/commands/workflow.py:115
# Component id: og.source.ass_ade.workflow_trust_gate
from __future__ import annotations

__version__ = "0.1.0"

def workflow_trust_gate(
    agent_id: str = typer.Argument(..., help="Agent ID to gate-check."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Multi-step agent trust gating: identity → sybil → trust → reputation → verdict."""
    from ass_ade.nexus.errors import NexusError
    from ass_ade.workflows import trust_gate

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = trust_gate(client, agent_id)
    except NexusError as exc:
        console.print(f"[red]Workflow error: {exc.detail}[/red]")
        raise typer.Exit(code=3) from exc
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    if json_out:
        _print_json(result.model_dump())
    else:
        color = {"ALLOW": "green", "WARN": "yellow", "DENY": "red"}.get(
            result.verdict, "white"
        )
        console.print(f"[{color}]Verdict: {result.verdict}[/{color}]")
        console.print(f"  Agent ID: {result.agent_id}")
        console.print(f"  Trust Score: {result.trust_score}")
        console.print(f"  Reputation: {result.reputation_tier}")
        for step in result.steps:
            mark = "✓" if step.passed else "✗"
            console.print(f"  [{mark}] {step.name}: {step.detail}")
