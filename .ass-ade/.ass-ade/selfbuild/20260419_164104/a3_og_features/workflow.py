"""Workflow command group — hero workflows with trust gates, certification, and safe execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import typer
from rich.console import Console

from ass_ade.config import default_config_path, load_config
from ass_ade.nexus.client import NexusClient

console = Console()

CONFIG_OPTION = typer.Option(None, help="Path to the ASS-ADE config file.")
ALLOW_REMOTE_OPTION = typer.Option(
    False, help="Permit remote calls when profile is local."
)
REPO_PATH_OPTION = typer.Option(
    Path("."),
    exists=True,
    file_okay=False,
    dir_okay=True,
    help="Repo root to assess.",
)


def _resolve_config(config_path: Path | None) -> tuple[Path, Any]:
    target = config_path or default_config_path()
    return target, load_config(target)


def _require_remote_access(settings: Any, allow_remote: bool) -> None:
    if settings.profile == "local" and not allow_remote:
        console.print(
            "Remote AAAA-Nexus calls are disabled in the local profile. "
            "Use --allow-remote or switch the profile to hybrid/premium."
        )
        raise typer.Exit(code=2)


def _nexus_err(exc: httpx.HTTPError) -> None:
    """Print a Nexus error message."""
    console.print(f"[red]Remote error:[/red] {exc}")


def _print_json(payload: Any, *, redact: bool = False) -> None:
    """Print payload as pretty JSON."""
    _ = redact
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump()
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
            console.print(json.dumps(parsed, indent=2), markup=False)
        except (json.JSONDecodeError, TypeError):
            console.print(payload, markup=False)
        return
    console.print(json.dumps(payload, indent=2), markup=False)


def register(app: typer.Typer) -> None:
    """Register workflow commands on the provided app."""
    app.command("phase0-recon")(workflow_phase0_recon)
    app.command("trust-gate")(workflow_trust_gate)
    app.command("certify")(workflow_certify)
    app.command("safe-execute")(workflow_safe_execute)
    app.command("map-terrain")(workflow_map_terrain)


def workflow_phase0_recon(
    task_description: str = typer.Argument(..., help="Task to recon before execution."),
    source: list[str] = typer.Option(
        [], "--source", help="Official source URL already researched."
    ),
    path: Path = REPO_PATH_OPTION,
    max_files: int = typer.Option(20, help="Maximum relevant files to return."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Never Code Blind gate: repo recon plus required latest-doc source targets."""
    from ass_ade.recon import phase0_recon

    result = phase0_recon(
        task_description=task_description,
        working_dir=path,
        provided_sources=source,
        max_relevant_files=max_files,
    )

    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    color = "green" if result.verdict == "READY_FOR_PHASE_1" else "yellow"
    console.print(f"[{color}]Phase 0 Recon: {result.verdict}[/{color}]")
    if result.research_targets:
        console.print("[bold]Research targets:[/bold]")
        for target in result.research_targets:
            hint = f" ({target.suggested_url})" if target.suggested_url else ""
            console.print(f"  - {target.topic}{hint}")
    if result.codebase.relevant_files:
        console.print("[bold]Relevant files:[/bold]")
        for rel in result.codebase.relevant_files:
            console.print(f"  - {rel}")
    if result.required_actions:
        console.print("[bold]Required before code:[/bold]")
        for action in result.required_actions:
            console.print(f"  - {action}")
    console.print(f"Next: {result.next_action}")


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


def workflow_certify(
    text: str = typer.Argument(..., help="Text to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Multi-step output certification: hallucination → ethics → compliance → certify → lineage."""
    from ass_ade.nexus.errors import NexusError
    from ass_ade.workflows import certify_output

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = certify_output(client, text)
    except NexusError as exc:
        console.print(f"[red]Workflow error: {exc.detail}[/red]")
        raise typer.Exit(code=3) from exc
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    if json_out:
        _print_json(result.model_dump())
    else:
        color = "green" if result.passed else "red"
        console.print(f"[{color}]Passed: {result.passed}[/{color}]")
        console.print(f"  Certificate: {result.certificate_id or 'none'}")
        console.print(f"  Lineage: {result.lineage_id or 'none'}")
        console.print(f"  Hallucination: {result.hallucination_verdict}")
        console.print(f"  Ethics: {result.ethics_verdict}")
        console.print(f"  Compliance: {result.compliance_verdict}")


def workflow_safe_execute(
    tool_name: str = typer.Argument(..., help="MCP tool name to execute."),
    tool_input: str = typer.Argument("", help="Input to the tool."),
    agent_id: str | None = typer.Option(None, help="Agent ID for AEGIS proxy."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """AEGIS-wrapped MCP tool execution: shield → scan → proxy → certify."""
    from ass_ade.nexus.errors import NexusError
    from ass_ade.workflows import safe_execute

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = safe_execute(client, tool_name, tool_input, agent_id=agent_id)
    except NexusError as exc:
        console.print(f"[red]Workflow error: {exc.detail}[/red]")
        raise typer.Exit(code=3) from exc
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    if json_out:
        _print_json(result.model_dump())
    else:
        console.print(f"  Tool: {result.tool_name}")
        console.print(f"  Shield: {'✓' if result.shield_passed else '✗'}")
        console.print(f"  Prompt Scan: {'✓' if result.prompt_scan_passed else '✗'}")
        console.print(f"  Certificate: {result.certificate_id or 'none'}")


def workflow_map_terrain(
    task_description: str = typer.Argument(
        ..., help="Task to validate before execution."
    ),
    agent: list[str] = typer.Option([], "--agent", help="Required agent capability."),
    hook: list[str] = typer.Option([], "--hook", help="Required hook capability."),
    skill: list[str] = typer.Option([], "--skill", help="Required skill capability."),
    tool: list[str] = typer.Option([], "--tool", help="Required tool capability."),
    harness: list[str] = typer.Option(
        [], "--harness", help="Required harness capability."
    ),
    prompt: list[str] = typer.Option(
        [], "--prompt", help="Required prompt capability."
    ),
    instruction: list[str] = typer.Option(
        [], "--instruction", help="Required instruction capability."
    ),
    requirements_file: Path | None = typer.Option(
        None, help="JSON file with grouped required_capabilities."
    ),
    auto_invent: bool = typer.Option(
        False,
        "--auto-invent",
        help="Generate repo-native assets plus certified rebuild packets for missing capabilities within budget.",
    ),
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
        "prompts": list(prompt),
        "instructions": list(instruction),
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
            if value is None:
                continue
            if isinstance(value, str):
                required[key] = [value] if value.strip() else []
            elif isinstance(value, (list, tuple, set)):
                required[key] = [str(item) for item in value if str(item).strip()]

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
            console.print(
                f"  - {item.type}: {item.name} via {item.recommended_creation_tool}"
            )
    console.print(f"Next: {result.next_action}")
    if result.development_plan and result.development_plan.created_assets:
        console.print("[bold]Created development-plan assets:[/bold]")
        for path in result.development_plan.created_assets:
            console.print(f"  - {path}")
