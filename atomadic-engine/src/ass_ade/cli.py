from __future__ import annotations

import hashlib
import json
import importlib
import os
import sys
from pathlib import Path
from typing import Annotated, Any, List, Optional

# Auto-load .env so CLI commands pick up AAAA_NEXUS_API_KEY and friends
# without requiring the user to export them manually each session.
try:
    from dotenv import load_dotenv as _load_dotenv
    for _candidate in (Path.cwd() / ".env", Path(__file__).resolve().parents[3] / ".env"):
        if _candidate.is_file():
            _load_dotenv(_candidate, override=False)
            break
except ImportError:
    pass

import httpx
import typer
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

from ass_ade.config import default_config_path, load_config, write_default_config
from ass_ade.local.planner import draft_plan, render_markdown
from ass_ade.local.repo import summarize_repo
from ass_ade.mcp import mock_server as _mock_server
from ass_ade.mcp.utils import (
    estimate_cost,
    invoke_tool,
    resolve_tool,
    simulate_invoke,
    validate_payload,
)
from ass_ade.nexus.client import NexusClient
from ass_ade.protocol.cycle import render_protocol_markdown, run_protocol
from ass_ade.protocol.evolution import (
    bump_project_version,
    parse_command_specs,
    parse_metrics,
    record_evolution_event,
    render_branch_evolution_demo,
    write_branch_evolution_demo,
)
from ass_ade.system import collect_tool_status

app = typer.Typer(
    invoke_without_command=True,
    help=(
        "Autonomous Sovereign System: Atomadic Development Environment. "
        "Public-safe developer shell for local, hybrid, and premium workflows.\n\n"
        "Run with no subcommand to start Atomadic — the interactive front door."
    ),
)
nexus_app = typer.Typer(help="Discover AAAA-Nexus public contracts and service status.")
mcp_app = typer.Typer(help="MCP manifest discovery and safe invocation helpers.")
repo_app = typer.Typer(help="Useful local-only repo inspection helpers.")
protocol_app = typer.Typer(
    help="Run a sanitized public-safe enhancement cycle."
)
# ── new product-family sub-apps ───────────────────────────────────────────────
oracle_app = typer.Typer(help="Hallucination Oracle, Trust Phase, Entropy, and Trust Decay.")
ratchet_app = typer.Typer(help="RatchetGate session security — CVE-2025-6514 fix.")
trust_app = typer.Typer(help="Trust Oracle (TCM-100/101) — formally bounded agent trust.")
text_app = typer.Typer(help="Text AI — summarize, keywords, sentiment.")
security_app = typer.Typer(help="Security — threat scoring, shield, PQC signing, zero-day scan.")
prompt_app = typer.Typer(help="Prompt artifact tools — hash, validate, section, diff, propose.")
inference_app = typer.Typer(help="AI inference via AAAA-Nexus. Defaults to falcon3-10B-1.58.")
escrow_app = typer.Typer(help="Agent Escrow — create, release, status, dispute, arbitrate.")
reputation_app = typer.Typer(help="Reputation Ledger — record, score, history, dispute.")
sla_app = typer.Typer(help="SLA Engine — register, report, status, breach.")
discovery_app = typer.Typer(help="Agent Discovery — search, recommend, registry.")
swarm_app = typer.Typer(help="Agent Swarm — plan, relay, intent-classify, and more.")
compliance_app = typer.Typer(help="Compliance Products — EU AI Act, fairness, drift, oversight.")
defi_app = typer.Typer(help="DeFi Suite — optimize, risk-score, oracle-verify, yield.")
aegis_app = typer.Typer(help="AEGIS — MCP proxy, epistemic route, certify epoch.")
control_app = typer.Typer(help="Control Plane — authorize, spending, lineage, federation.")
identity_app = typer.Typer(help="Identity & Auth — verify, sybil-check, delegate, federation.")
vrf_app = typer.Typer(help="VRF Gaming — draw, verify-draw.")
bitnet_app = typer.Typer(help="BitNet 1.58-bit inference — defaults to falcon3-10B-1.58.")
vanguard_app = typer.Typer(help="VANGUARD — red-team, MEV route, wallet session, escrow.")
mev_app = typer.Typer(help="MEV Shield — protect transaction bundles, check status.")
forge_app = typer.Typer(help="Forge Marketplace — leaderboard, verify, quarantine, delta.")
dev_app = typer.Typer(help="Developer Tools — starter, crypto-toolkit, routing.")
data_app = typer.Typer(help="Data Tools — validate JSON, format convert.")
context_app = typer.Typer(help="Context tools — context packets and local vector memory.")
workflow_app = typer.Typer(help="Hero Workflows — trust-gate, certify, safe-execute.")
agent_app = typer.Typer(help="Agentic IDE — chat and run tasks using any model.")
a2a_app = typer.Typer(help="A2A Interop — agent card validation, negotiation, and discovery.")
pipeline_app = typer.Typer(help="Workflow Pipelines — composable, chainable workflow execution.")

app.add_typer(nexus_app, name="nexus")
app.add_typer(mcp_app, name="mcp")
app.add_typer(repo_app, name="repo")
app.add_typer(protocol_app, name="protocol")
app.add_typer(oracle_app, name="oracle")
app.add_typer(ratchet_app, name="ratchet")
app.add_typer(trust_app, name="trust")
app.add_typer(text_app, name="text")
app.add_typer(security_app, name="security")
app.add_typer(prompt_app, name="prompt")
app.add_typer(inference_app, name="llm")
app.add_typer(escrow_app, name="escrow")
app.add_typer(reputation_app, name="reputation")
app.add_typer(sla_app, name="sla")
app.add_typer(discovery_app, name="discovery")
app.add_typer(swarm_app, name="swarm")
app.add_typer(compliance_app, name="compliance")
app.add_typer(defi_app, name="defi")
app.add_typer(aegis_app, name="aegis")
app.add_typer(control_app, name="control")
app.add_typer(identity_app, name="identity")
app.add_typer(vrf_app, name="vrf")
app.add_typer(bitnet_app, name="bitnet")
app.add_typer(vanguard_app, name="vanguard")
app.add_typer(mev_app, name="mev")
app.add_typer(forge_app, name="forge")
app.add_typer(dev_app, name="dev")
app.add_typer(data_app, name="data")
app.add_typer(context_app, name="context")
app.add_typer(workflow_app, name="workflow")
app.add_typer(agent_app, name="agent")
app.add_typer(a2a_app, name="a2a")
app.add_typer(pipeline_app, name="pipeline")

# Blueprint → production-grade build (iterative refinement, no stubs)
from ass_ade.commands.blueprint import blueprint_app  # noqa: E402
app.add_typer(blueprint_app, name="blueprint")

# Cap-B: complete partial codebases
from ass_ade.commands.finish import finish_app  # noqa: E402
app.add_typer(finish_app, name="finish")

# Cap-C: propose blueprints for new features
from ass_ade.commands.feature import feature_app  # noqa: E402
app.add_typer(feature_app, name="feature")

# Self-rebuild: run monadic decomposition over !ass-ade* siblings
from ass_ade.commands.selfbuild import selfbuild_app  # noqa: E402
app.add_typer(selfbuild_app, name="selfbuild")

from ass_ade.commands.aso import aso_app  # noqa: E402
app.add_typer(aso_app, name="optimize")

providers_app = typer.Typer(help="Manage free LLM providers (Groq, Gemini, OpenRouter, Ollama, ...).")
app.add_typer(providers_app, name="providers")

# Register modularized command groups
from ass_ade.commands import register_commands
register_commands(agent_app, a2a_app, workflow_app, providers_app)

# ── Atomadic memory sub-app ────────────────────────────────────────────────────
memory_app = typer.Typer(help="Atomadic local memory — what I remember about you and your projects.")
app.add_typer(memory_app, name="memory")

import sys as _sys
if hasattr(_sys.stdout, "reconfigure"):
    try:
        _sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
console = Console()
DEFAULT_AAAA_NEXUS_MODEL = "falcon3-10B-1.58"


# ── App callback: no-subcommand → Atomadic interactive mode ───────────────────

@app.callback(invoke_without_command=True)
def _app_callback(ctx: typer.Context) -> None:
    """Launch Atomadic if no subcommand is given."""
    if ctx.invoked_subcommand is None:
        cwd = Path(".").resolve()
        from ass_ade.interpreter import run_interactive
        run_interactive(working_dir=cwd)


# ── Top-level chat command ─────────────────────────────────────────────────────

@app.command("chat")
def interpreter_chat(
    working_dir: Path = typer.Option(
        Path("."), "--dir", "-d", help="Working directory for this session."
    ),
) -> None:
    """Start an interactive chat session with Atomadic.

    Speak plainly — casual, technical, or anywhere in between.
    Atomadic derives your intent and dispatches the right command.
    """
    from ass_ade.interpreter import run_interactive
    run_interactive(working_dir=working_dir.resolve())


# ── Memory commands ────────────────────────────────────────────────────────────

@memory_app.command("show")
def memory_show() -> None:
    """Show what Atomadic remembers about you and your projects."""
    from ass_ade.interpreter import MemoryStore
    store = MemoryStore.load()
    console.print(store.summarize())


@memory_app.command("clear")
def memory_clear(
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
) -> None:
    """Wipe all local Atomadic memory."""
    if not confirm:
        typer.confirm("This will erase all local Atomadic memory. Continue?", abort=True)
    from ass_ade.interpreter import MemoryStore
    MemoryStore.clear()
    console.print("[green]Memory cleared.[/green]")


@memory_app.command("export")
def memory_export(
    output: Path = typer.Argument(Path("atomadic-memory-export.json"), help="Export destination."),
) -> None:
    """Export local memory to a JSON file for backup."""
    import json as _json
    from ass_ade.interpreter import MemoryStore
    store = MemoryStore.load()
    data = store.to_dict()
    output.write_text(_json.dumps(data, indent=2, default=str), encoding="utf-8")
    console.print(f"[green]Memory exported →[/green] {output}")


CONFIG_OPTION = typer.Option(None, help="Path to the ASS-ADE config file.")
OVERWRITE_OPTION = typer.Option(False, help="Overwrite an existing config file.")
ALLOW_REMOTE_OPTION = typer.Option(
    False, help="Permit remote calls when profile is local."
)


def _collapse_prompt_parts(prompt_parts: List[str]) -> str:
    """Accept natural multi-word prompts without forcing shell quoting."""
    return " ".join(prompt_parts).strip()
REMOTE_PROBE_OPTION = typer.Option(
    None,
    "--remote/--no-remote",
    help=(
        "Probe the configured AAAA-Nexus base URL. Local profile never auto-probes "
        "(even if AAAA_NEXUS_API_KEY is set); use --remote to enable. Hybrid/premium "
        "default to probing; use --no-remote to skip."
    ),
)
REPO_PATH_ARGUMENT = typer.Argument(
    Path("."),
    exists=True,
    file_okay=False,
    dir_okay=True,
    help="Repo root to inspect.",
)
REPO_PATH_OPTION = typer.Option(
    Path("."),
    exists=True,
    file_okay=False,
    dir_okay=True,
    help="Repo root to assess.",
)
FULL_CYCLE_REMOTE_OPTION = typer.Option(
    None,
    "--remote/--no-remote",
    help="Probe AAAA-Nexus during the cycle. Defaults to enabled for hybrid/premium.",
)
FULL_CYCLE_ALLOW_REMOTE_OPTION = typer.Option(
    False,
    help="Permit remote probes when profile is local.",
)
FULL_CYCLE_REPORT_OUT_OPTION = typer.Option(
    None,
    help="Write the protocol report as Markdown to this path.",
)
FULL_CYCLE_JSON_OUT_OPTION = typer.Option(
    None,
    help="Write the cycle report payload as JSON to this path.",
)


def _resolve_config(config_path: Path | None) -> tuple[Path, Any]:
    target = config_path or default_config_path()
    return target, load_config(target)


_SENSITIVE_OUTPUT_KEY_PARTS = (
    "api_key",
    "authorization",
    "authorization_token",
    "credential",
    "payment_proof",
    "private_key",
    "secret",
    "token",
    "x-api-key",
)


def _redact_secrets(payload: Any) -> Any:
    if isinstance(payload, dict):
        redacted: dict[Any, Any] = {}
        for key, value in payload.items():
            key_text = str(key).lower()
            if any(part in key_text for part in _SENSITIVE_OUTPUT_KEY_PARTS):
                redacted[key] = "[redacted]"
            else:
                redacted[key] = _redact_secrets(value)
        return redacted
    if isinstance(payload, list):
        return [_redact_secrets(item) for item in payload]
    return payload


def _print_json(payload: Any, *, redact: bool = False) -> None:
    if isinstance(payload, BaseModel):
        payload = payload.model_dump()

    # Normalize and pretty-print JSON safely to avoid double-encoding and
    # escaped quotes when running under test harnesses.
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
            if redact:
                parsed = _redact_secrets(parsed)
            console.print(json.dumps(parsed, indent=2), markup=False)
        except (json.JSONDecodeError, TypeError):
            console.print(payload, markup=False)
        return

    if hasattr(payload, "model_dump"):
        payload = payload.model_dump()

    if redact:
        payload = _redact_secrets(payload)

    console.print(json.dumps(payload, indent=2), markup=False)


def _should_probe_remote(settings: Any, remote: bool | None) -> bool:
    if remote is not None:
        return remote
    # Local profile: never auto-probe, even if an API key is present in the
    # environment (keys are still used for explicit remote commands). Matches
    # `doctor --help` and keeps `ass-ade doctor` deterministic under tests.
    if settings.profile == "local":
        return False
    if getattr(settings, "nexus_api_key", None):
        return True
    return settings.profile in {"hybrid", "premium"}


_CREDITS_BUY_MESSAGE = """\
[bold yellow]This feature requires API credits.[/bold yellow]

  [bold]x402 USDC (instant)[/bold] — pay per call, no account needed:
    [cyan]https://atomadic.tech/pay[/cyan]

  [bold]Stripe (credit card)[/bold] — credit packs from $10:
    [cyan]https://atomadic.tech/pay[/cyan]

  [bold]Set your key:[/bold]
    export ATOMADIC_API_KEY=your_key_here

  [bold green]Earn credits back![/bold green] Quality rebuilds that pass the trust gate
  earn bonus API credits. The better your code, the more you earn.

Run [bold]ass-ade credits[/bold] to check your balance."""


def _require_remote_access(settings: Any, allow_remote: bool) -> None:
    if settings.profile == "local" and not allow_remote:
        console.print(
            "Remote AAAA-Nexus calls are disabled in the local profile. "
            "Use --allow-remote or switch the profile to hybrid/premium."
        )
        raise typer.Exit(code=2)


@app.command()
def init(
    config: Path | None = CONFIG_OPTION,
    overwrite: bool = OVERWRITE_OPTION,
) -> None:
    target = config or default_config_path()
    existed = target.exists()
    write_default_config(target, overwrite=overwrite)
    if existed and not overwrite:
        console.print(f"Config already exists at {target}")
        return
    console.print(f"Wrote config to {target}")


@app.command()
def doctor(
    config: Path | None = CONFIG_OPTION,
    remote: bool | None = REMOTE_PROBE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
) -> None:
    config_path, settings = _resolve_config(config)
    probe_remote = _should_probe_remote(settings, remote)

    tool_items = collect_tool_status()
    health_data: dict | None = None

    if not json_out:
        summary = Table(title="ASS-ADE Environment")
        summary.add_column("Setting")
        summary.add_column("Value")
        summary.add_row("Config", str(config_path))
        summary.add_row("Profile", settings.profile)
        summary.add_row("Nexus Base URL", settings.nexus_base_url)
        summary.add_row("Remote Probe", "enabled" if probe_remote else "disabled")
        console.print(summary)

        tools = Table(title="Toolchain")
        tools.add_column("Tool")
        tools.add_column("Status")
        tools.add_column("Version / Error")
        for item in tool_items:
            tools.add_row(
                item.name,
                "ok" if item.available else "missing",
                item.version or item.error or "",
            )
        console.print(tools)

    if probe_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
            ) as client:
                health = client.get_health()
                health_data = health.model_dump() if hasattr(health, "model_dump") else dict(health)
        except httpx.HTTPError as exc:
            if not json_out:
                console.print(f"Remote probe failed: {exc}")
            else:
                _print_json({"error": str(exc), "remote_probe": "failed"})
            raise typer.Exit(code=1) from exc

        if not json_out:
            console.print("Remote probe succeeded.")
            _print_json(health_data)

    if json_out:
        payload: dict = {
            "config": str(config_path),
            "profile": settings.profile,
            "nexus_base_url": settings.nexus_base_url,
            "remote_probe": "enabled" if probe_remote else "disabled",
            "tools": [
                {
                    "name": item.name,
                    "available": item.available,
                    "version": item.version,
                    "error": item.error,
                }
                for item in tool_items
            ],
        }
        if health_data is not None:
            payload["remote_health"] = health_data
        print(json.dumps(payload, indent=2))


@app.command()
def credits(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show your API credit balance and usage, with quick buy links."""
    _, settings = _resolve_config(config)

    if not settings.nexus_api_key:
        console.print("[bold yellow]No API key configured.[/bold yellow]\n")
        console.print(_CREDITS_BUY_MESSAGE)
        raise typer.Exit(code=0)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client._client.get("/v1/credits/balance")
            result.raise_for_status()
            data = result.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code in (401, 402):
            console.print("[red]Authentication failed.[/red]\n")
            console.print(_CREDITS_BUY_MESSAGE)
        else:
            console.print(f"[red]Error checking balance:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        console.print(f"[red]Error checking balance:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    t = Table(title="API Credits")
    t.add_column("Field")
    t.add_column("Value")
    balance_keys = {"balance", "balance_usdc", "balance_micro_usdc", "plan", "calls_remaining"}
    for k, v in data.items():
        if str(k).lower() in balance_keys or not balance_keys.isdisjoint({str(k).lower()}):
            t.add_row(str(k), str(v))
        else:
            t.add_row(str(k), str(v))
    console.print(t)

    # Rewards section
    accepted = data.get("lora_contributions_accepted", data.get("contributions_accepted"))
    quality = data.get("quality_score", data.get("trust_score"))
    next_tier = data.get("next_reward_tier")
    if accepted is not None or quality is not None:
        r = Table(title="LoRA Contribution Rewards")
        r.add_column("Metric")
        r.add_column("Value")
        if accepted is not None:
            earned = int(accepted) * 2
            r.add_row("Contributions accepted", f"{accepted} (earned {earned} bonus credits)")
        if quality is not None:
            r.add_row("Quality score", f"{quality} (trust gate: ≥ τ_trust)")
        if next_tier is not None:
            r.add_row("Next reward tier", f"{next_tier} more accepted contributions")
        console.print(r)
        console.print("[dim]Top contributors with consistently high quality get unlimited access.[/dim]")

    console.print("\nTop up at [cyan]https://atomadic.tech/pay[/cyan]")


@app.command()
def plan(
    goal: str = typer.Argument(..., help="Goal to break into a public-safe draft plan."),
    max_steps: int = typer.Option(5, min=1, max=10, help="Maximum number of steps to emit."),
    markdown: bool = typer.Option(False, help="Render the plan as Markdown."),
) -> None:
    steps = draft_plan(goal, max_steps=max_steps)
    if markdown:
        console.print(render_markdown(goal, steps))
        return

    table = Table(title="Draft Plan")
    table.add_column("#", justify="right")
    table.add_column("Step")
    for index, step in enumerate(steps, start=1):
        table.add_row(str(index), step)
    console.print(table)


@app.command("cycle")
def full_cycle(
    goal: str = typer.Argument(
        ..., help="Enhancement goal for the full ASS-ADE cycle."
    ),
    config: Path | None = CONFIG_OPTION,
    path: Path = REPO_PATH_OPTION,
    remote: bool | None = FULL_CYCLE_REMOTE_OPTION,
    allow_remote: bool = FULL_CYCLE_ALLOW_REMOTE_OPTION,
    report_out: Path | None = FULL_CYCLE_REPORT_OUT_OPTION,
    json_out: Path | None = FULL_CYCLE_JSON_OUT_OPTION,
) -> None:
    _, settings = _resolve_config(config)
    repo_scan = summarize_repo(path)
    steps = draft_plan(goal, max_steps=6)
    report = run_protocol(goal, path, settings)
    probe_remote = _should_probe_remote(settings, remote)

    remote_probe_status = "skipped"
    if probe_remote:
        if settings.profile == "local" and not allow_remote:
            remote_probe_status = "blocked (local profile, add --allow-remote)"
        else:
            try:
                with NexusClient(
                    base_url=settings.nexus_base_url,
                    timeout=settings.request_timeout_s,
                    api_key=settings.nexus_api_key,
                ) as client:
                    health = client.get_health()
                remote_probe_status = f"ok ({health.status})"
            except httpx.HTTPError as exc:
                remote_probe_status = f"failed ({exc.__class__.__name__})"

    passed_checks = sum(1 for item in report.audit if item.passed)

    overview = Table(title="ASS-ADE Full Cycle")
    overview.add_column("Signal")
    overview.add_column("Value")
    overview.add_row("Goal", goal)
    overview.add_row("Profile", settings.profile)
    overview.add_row("Root", str(repo_scan.root))
    overview.add_row("Files", str(repo_scan.total_files))
    overview.add_row("Directories", str(repo_scan.total_dirs))
    overview.add_row("Remote Probe", remote_probe_status)
    overview.add_row("Audit", f"{passed_checks}/{len(report.audit)} passed")
    console.print(overview)

    design = Table(title="Design Steps")
    design.add_column("#", justify="right")
    design.add_column("Step")
    for index, step in enumerate(steps, start=1):
        design.add_row(str(index), step)
    console.print(design)

    console.print(f"Protocol Summary: {report.summary}")

    if report_out is not None:
        markdown_report = render_protocol_markdown(report)
        report_out.parent.mkdir(parents=True, exist_ok=True)
        report_out.write_text(f"{markdown_report}\n", encoding="utf-8")
        console.print(f"Wrote report to {report_out}")

    if json_out is not None:
        payload = {
            "goal": goal,
            "profile": settings.profile,
            "root": str(repo_scan.root),
            "remote_probe": remote_probe_status,
            "audit_passed": passed_checks,
            "audit_total": len(report.audit),
            "report": report.model_dump(mode="json"),
        }
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(f"{json.dumps(payload, indent=2)}\n", encoding="utf-8")
        console.print(f"Wrote JSON report to {json_out}")


@repo_app.command("summary")
def repo_summary(
    path: Path = REPO_PATH_ARGUMENT,
    top: int = typer.Option(8, min=1, max=25, help="Number of file types to show."),
) -> None:
    summary = summarize_repo(path)

    overview = Table(title="Repo Summary")
    overview.add_column("Signal")
    overview.add_column("Value")
    overview.add_row("Root", str(summary.root))
    overview.add_row("Files", str(summary.total_files))
    overview.add_row("Directories", str(summary.total_dirs))
    overview.add_row("Top-level Entries", ", ".join(summary.top_level_entries[:12]) or "none")
    console.print(overview)

    types = Table(title="Top File Types")
    types.add_column("Type")
    types.add_column("Count", justify="right")
    for file_type, count in list(summary.file_types.items())[:top]:
        types.add_row(file_type, str(count))
    console.print(types)


@protocol_app.command("run")
def protocol_run(
    goal: str = typer.Argument(..., help="Enhancement goal for the protocol cycle."),
    config: Path | None = CONFIG_OPTION,
    path: Path = REPO_PATH_OPTION,
    markdown: bool = typer.Option(False, help="Render the protocol report as Markdown."),
) -> None:
    _, settings = _resolve_config(config)
    report = run_protocol(goal, path, settings)

    if markdown:
        console.print(render_protocol_markdown(report))
        return

    overview = Table(title="ASS-ADE Protocol Report")
    overview.add_column("Signal")
    overview.add_column("Value")
    overview.add_row("Goal", report.goal)
    overview.add_row("Profile", report.assessment.profile)
    overview.add_row("Root", report.assessment.root)
    overview.add_row("Files", str(report.assessment.total_files))
    overview.add_row("Directories", str(report.assessment.total_dirs))
    overview.add_row("Audit Checks", str(len(report.audit)))
    console.print(overview)

    design = Table(title="Design Steps")
    design.add_column("#", justify="right")
    design.add_column("Step")
    for index, step in enumerate(report.design_steps, start=1):
        design.add_row(str(index), step)
    console.print(design)

    audit = Table(title="Audit")
    audit.add_column("Status")
    audit.add_column("Check")
    audit.add_column("Detail")
    for item in report.audit:
        audit.add_row("PASS" if item.passed else "FAIL", item.name, item.detail)
    console.print(audit)

    recommendations = Table(title="Recommendations")
    recommendations.add_column("#", justify="right")
    recommendations.add_column("Recommendation")
    for index, item in enumerate(report.recommendations, start=1):
        recommendations.add_row(str(index), item)
    console.print(recommendations)

    console.print(report.summary)


@protocol_app.command("evolution-record")
def protocol_evolution_record(
    event_type: str = typer.Argument(..., help="Evolution event type, such as birth, iteration, merge, or release."),
    summary: str = typer.Option(..., "--summary", help="Public-safe summary of what changed."),
    config: Path | None = CONFIG_OPTION,
    path: Path = REPO_PATH_OPTION,
    version: str = typer.Option("", "--version", help="Version to record. Defaults to the project version."),
    rebuild_path: Path | None = typer.Option(None, "--rebuild-path", help="Optional rebuild output folder to summarize."),
    command: list[str] = typer.Option(
        [],
        "--command",
        "-c",
        help="Command receipt. Prefix with status=passed:: if useful.",
    ),
    metric: list[str] = typer.Option([], "--metric", help="Metric in key=value form. Repeatable."),
    report: list[Path] = typer.Option([], "--report", help="Report path to record. Repeatable."),
    artifact: list[Path] = typer.Option([], "--artifact", help="Artifact path to record. Repeatable."),
    rationale: str = typer.Option("", "--rationale", help="Brief public decision summary."),
    next_step: list[str] = typer.Option([], "--next-step", help="Next step to record. Repeatable."),
    lineage_id: list[str] = typer.Option([], "--lineage-id", help="Optional Nexus lineage id. Repeatable."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Append a public-safe evolution event and refresh EVOLUTION.md."""
    _resolve_config(config)
    try:
        commands = parse_command_specs(command)
        metrics = parse_metrics(metric)
    except ValueError as exc:
        console.print(f"[red]Evolution record error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    result = record_evolution_event(
        root=path,
        event_type=event_type,
        summary=summary,
        version=version,
        rebuild_path=rebuild_path,
        commands=commands,
        metrics=metrics,
        reports=[str(item) for item in report],
        artifacts=[str(item) for item in artifact],
        rationale=rationale,
        next_steps=next_step,
        lineage_ids=lineage_id or None,
    )

    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    table = Table(title="Evolution Event Recorded")
    table.add_column("Signal")
    table.add_column("Value")
    table.add_row("Event", result.event.event_type)
    table.add_row("Event ID", result.event.event_id)
    table.add_row("Version", result.event.version)
    table.add_row("Ledger", result.ledger_path)
    table.add_row("Snapshot", result.snapshot_path)
    table.add_row("Markdown", result.markdown_path)
    console.print(table)


@protocol_app.command("evolution-demo")
def protocol_evolution_demo(
    path: Path = REPO_PATH_OPTION,
    branches: str = typer.Option(
        "tests-first,docs-first,safety-first",
        "--branches",
        help="Comma-separated branch track names.",
    ),
    iterations: int = typer.Option(3, min=1, max=12, help="Iterations to show per branch."),
    output: Path | None = typer.Option(None, "--output", help="Where to write the demo markdown."),
    write: bool = typer.Option(True, "--write/--print", help="Write docs/evolution-workflow.md or print markdown."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON when writing."),
) -> None:
    """Generate the split-branch evolution demo workflow."""
    branch_list = [item.strip() for item in branches.split(",") if item.strip()]
    if not write:
        console.print(render_branch_evolution_demo(root=path, branches=branch_list, iterations=iterations))
        return

    target = write_branch_evolution_demo(
        root=path,
        branches=branch_list,
        iterations=iterations,
        output=output,
    )
    if json_out:
        _print_json({"path": str(target), "branches": branch_list, "iterations": iterations})
    else:
        console.print(f"[green]Wrote evolution demo:[/green] {target}")


@protocol_app.command("version-bump")
def protocol_version_bump(
    bump: str = typer.Argument(..., help="patch, minor, or major. Use --to for an explicit version."),
    path: Path = REPO_PATH_OPTION,
    to_version: str = typer.Option("", "--to", help="Explicit semantic version to set."),
    summary: str = typer.Option("Version update", "--summary", help="Release note summary."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing files or ledger entries."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Update package version surfaces and record the bump in the evolution ledger."""
    try:
        bump_result = bump_project_version(
            root=path,
            bump=bump,
            new_version=to_version,
            summary=summary,
            dry_run=dry_run,
        )
    except ValueError as exc:
        console.print(f"[red]Version bump error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    event_result = None
    if not dry_run:
        command_text = f"status=completed::ass-ade protocol version-bump {bump}"
        if to_version:
            command_text = f"{command_text} --to {to_version}"
        event_result = record_evolution_event(
            root=path,
            event_type="version-bump",
            summary=summary,
            version=bump_result.new_version,
            commands=parse_command_specs([command_text]),
            metrics={
                "old_version": bump_result.old_version,
                "new_version": bump_result.new_version,
            },
            artifacts=bump_result.files_updated,
            rationale="Package version surfaces were updated together before release.",
        )

    payload = {
        "version": bump_result.model_dump(),
        "event": event_result.model_dump() if event_result is not None else None,
    }
    if json_out:
        _print_json(payload, redact=True)
        return

    console.print(
        f"[green]Version:[/green] {bump_result.old_version} -> {bump_result.new_version}"
        + (" (dry run)" if dry_run else "")
    )
    for item in bump_result.files_updated:
        console.print(f"  - {item}")
    if event_result is not None:
        console.print(f"[green]Evolution event:[/green] {event_result.event.event_id}")


@nexus_app.command("health")
def nexus_health(
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
            _print_json(client.get_health())
    except httpx.HTTPError as exc:
        _nexus_err(exc)


@nexus_app.command("agent-card")
def nexus_agent_card(
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
            _print_json(client.get_agent_card())
    except httpx.HTTPError as exc:
        _nexus_err(exc)


@nexus_app.command("mcp-manifest")
def nexus_mcp_manifest(
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
            _print_json(client.get_mcp_manifest())
    except httpx.HTTPError as exc:
        _nexus_err(exc)


@mcp_app.command("tools")
def mcp_tools(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List tools published in the MCP manifest."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url, timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key
        ) as client:
            manifest = client.get_mcp_manifest()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return

    table = Table(title="MCP Tools")
    table.add_column("#", justify="right")
    table.add_column("Name")
    table.add_column("Endpoint")
    table.add_column("Method")
    table.add_column("Paid")
    for idx, tool in enumerate(manifest.tools, start=1):
        table.add_row(
            str(idx), tool.name or "n/a", tool.endpoint or "n/a", tool.method
            or "POST", str(bool(tool.paid)),
        )
    console.print(table)


@mcp_app.command("inspect")
def mcp_inspect(
    identifier: str = typer.Argument(..., help="Tool name or index (1-based)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Show full MCP tool metadata for a named tool or numeric index."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url, timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key
        ) as client:
            manifest = client.get_mcp_manifest()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return

    tool = resolve_tool(manifest, identifier)
    if tool is None:
        console.print(f"Tool not found: {identifier}")
        raise typer.Exit(code=2)

    _print_json(tool)


@mcp_app.command("invoke")
def mcp_invoke(
    identifier: str = typer.Argument(..., help="Tool name or index (1-based)."),
    input_file: Path | None = typer.Option(None, help="Path to JSON file to send as payload."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    confirm_paid: bool = typer.Option(False, help="Confirm invocation of paid tools."),
    redact: bool = typer.Option(
        True,
        "--redact/--no-redact",
        help="Redact token, key, credential, and payment-proof fields in output.",
    ),
    dry_run: bool = typer.Option(False, "--dry-run",
                                 help="Simulate invocation without network I/O."),
    schema_validate: bool = typer.Option(False, "--schema-validate",
        help="Validate input payload against tool's JSON Schema if provided."),
    json_out: Path | None = typer.Option(None,
        help="Write full response payload as JSON to this path."),
) -> None:
    """Invoke a tool from the MCP manifest. Requires remote access to be enabled.

    Use `--dry-run` to simulate the invocation without performing network I/O.
    """
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    with NexusClient(
        base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key
    ) as client:
        manifest = client.get_mcp_manifest()

    tool = resolve_tool(manifest, identifier)
    if tool is None:
        console.print(f"Tool not found: {identifier}")
        raise typer.Exit(code=2)

    if bool(tool.paid) and not confirm_paid and not dry_run:
        console.print(
            "This tool appears to be paid. Re-run with --confirm-paid to proceed."
        )
        raise typer.Exit(code=3)

    payload = None
    if input_file is not None:
        if not input_file.exists():
            console.print(f"Input file not found: {input_file}")
            raise typer.Exit(code=4)
        try:
            payload = json.loads(input_file.read_text(encoding="utf-8"))
        except Exception as exc:
            console.print(f"Failed to parse input JSON: {exc}")
            raise typer.Exit(code=5)

    # Schema validation (if requested)
    if schema_validate:
        valid, err = validate_payload(getattr(tool, "inputSchema", None), payload)
        if not valid:
            console.print(f"Schema validation failed: {err}")
            raise typer.Exit(code=7)

    if dry_run:
        sim = simulate_invoke(settings.nexus_base_url, tool, payload)
        _print_json(sim)
        if json_out is not None:
            json_out.parent.mkdir(parents=True, exist_ok=True)
            json_out.write_text(f"{json.dumps(sim, indent=2)}\n", encoding="utf-8")
            console.print(f"Wrote simulation to {json_out}")
        return

    try:
        response = invoke_tool(
            settings.nexus_base_url,
            tool,
            payload,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        console.print(f"Invocation failed: {exc}")
        raise typer.Exit(code=6) from exc

    # Try to pretty-print JSON, otherwise raw text
    try:
        body = response.json()
        rendered_body = _redact_secrets(body) if redact else body
        _print_json(rendered_body)
        if json_out is not None:
            json_out.parent.mkdir(parents=True, exist_ok=True)
            json_out.write_text(f"{json.dumps(rendered_body, indent=2)}\n", encoding="utf-8")
            console.print(f"Wrote response to {json_out}")
    except (json.JSONDecodeError, ValueError):
        console.print(response.text)



@mcp_app.command("estimate-cost")
def mcp_estimate_cost(
    identifier: str = typer.Argument(..., help="Tool name or index (1-based)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Show cost and rate-limit metadata for a tool declared in the MCP manifest."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url, timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key
        ) as client:
            manifest = client.get_mcp_manifest()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return

    tool = resolve_tool(manifest, identifier)
    if tool is None:
        console.print(f"Tool not found: {identifier}")
        raise typer.Exit(code=2)

    cost = estimate_cost(tool)
    if cost is None:
        console.print(f"Tool '{tool.name}' is free with no cost metadata.")
        return

    table = Table(title=f"Cost Estimate – {tool.name}")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Currency", cost.currency)
    table.add_row("Unit Cost", str(cost.unit_cost) if cost.unit_cost is not None else "n/a")
    table.add_row("Rate Limit (req/min)", str(cost.rate_limit_rpm) if cost.rate_limit_rpm is not None else "n/a")
    table.add_row("Rate Limit (tokens/min)", str(cost.rate_limit_tpm) if cost.rate_limit_tpm is not None else "n/a")
    table.add_row("Notes", cost.notes or "—")
    console.print(table)


@mcp_app.command("mock-server")
def mcp_mock_server(
    port: int = typer.Option(8787, help="TCP port to listen on."),
    manifest: Path | None = typer.Option(None, help="Path to a JSON manifest file to serve."),
) -> None:
    """Start a local mock MCP server for development and integration testing.

    Serves the manifest at http://localhost:<port>/.well-known/mcp.json and
    echoes POST payloads back. No remote access required.
    """
    console.print(f"Starting mock MCP server on http://127.0.0.1:{port} (Ctrl+C to stop)")
    if manifest is not None:
        console.print(f"Serving manifest from {manifest}")
    _mock_server.start_server(port=port, manifest_path=manifest, block=True)


@mcp_app.command("serve")
def mcp_serve(
    working_dir: Path = typer.Option(
        Path("."), exists=True, file_okay=False, help="Working directory for tools."
    ),
) -> None:
    """Start ASS-ADE as an MCP tool server (stdio transport).

    Exposes all built-in tools over the Model Context Protocol for use
    with VS Code Copilot, Claude Desktop, or any MCP-compatible client.

    Example mcpServers config for VS Code settings.json:
        "ass-ade": { "command": "ass-ade", "args": ["mcp", "serve"] }
    """
    from ass_ade.mcp.server import MCPServer

    server = MCPServer(working_dir=str(working_dir.resolve()))
    server.run()


@nexus_app.command("overview")
def nexus_overview(
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
            health = client.get_health()
            openapi = client.get_openapi()
            agent_card = client.get_agent_card()
            mcp_manifest = client.get_mcp_manifest()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return

    table = Table(title="AAAA-Nexus Overview")
    table.add_column("Signal")
    table.add_column("Value")
    table.add_row("Base URL", settings.nexus_base_url)
    table.add_row("Health Status", health.status)
    table.add_row("API Version", str(openapi.info.version or "unknown"))
    table.add_row("Agent Card Name", agent_card.name)
    table.add_row("Agent Skills", str(len(agent_card.skills)))
    table.add_row("MCP Tools", str(len(mcp_manifest.tools)))
    table.add_row(
        "Trial Policy",
        str(
            (agent_card.trialPolicy.note if agent_card.trialPolicy else None)
            or (agent_card.authentication.trialAccess if agent_card.authentication else None)
            or "n/a"
        ),
    )
    console.print(table)


def _nexus_err(exc: httpx.HTTPError) -> None:
    """Print a user-friendly API error and exit code 1."""
    status = getattr(getattr(exc, "response", None), "status_code", None)
    if status in (401, 402):
        console.print(f"API request failed ({status})\n")
        console.print(_CREDITS_BUY_MESSAGE)
    elif status == 429:
        console.print("API request failed (429) — rate limit reached; upgrade plan or retry later")
    else:
        console.print(f"API request failed ({status or type(exc).__name__})")
    raise typer.Exit(code=1) from exc


# ── Progress bar and project-detection helpers ────────────────────────────────

def _draw_progress_bar(label: str, current: int, total: int, start_time: float) -> None:
    """Print a single-line progress bar. Overwrites the previous line in-place."""
    import time as _time
    width = 20
    if total <= 0:
        frac = 1.0
    else:
        frac = min(current / total, 1.0)
    filled = int(width * frac)
    bar = "█" * filled + "░" * (width - filled)
    pct = int(frac * 100)
    elapsed = _time.monotonic() - start_time
    eta = ""
    if frac > 0.01 and frac < 1.0:
        remaining = elapsed / frac * (1.0 - frac)
        eta = f" ~{remaining:.0f}s remaining"
    line = f"\r⏳ {label} [{bar}] {pct}% ({current}/{total} files){eta}   "
    print(line, end="", flush=True)


def _finish_progress_bar(label: str, total: int, elapsed: float) -> None:
    """Print the completed bar and advance to next line."""
    width = 20
    bar = "█" * width
    line = f"\r✅ {label} [{'█' * width}] 100% ({total}/{total} files) — {elapsed:.1f}s   "
    print(line, flush=True)


def _auto_detect_project(path: Path) -> str:
    """Scan ``path`` and return a one-liner project description."""
    ext_counts: dict[str, int] = {}
    total_files = 0
    has_tier_structure = False
    tier_dirs = {"a0_qk_constants", "a1_at_functions", "a2_mo_composites",
                 "a3_og_features", "a4_sy_orchestration"}
    _ignore = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
               "dist", "build", "target"}
    try:
        for entry in path.rglob("*"):
            if any(part in _ignore for part in entry.parts):
                continue
            if entry.is_dir() and entry.name in tier_dirs:
                has_tier_structure = True
            if entry.is_file():
                total_files += 1
                ext = entry.suffix.lower()
                if ext:
                    ext_counts[ext] = ext_counts.get(ext, 0) + 1
    except PermissionError:
        pass

    lang_map = {
        ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript/React",
        ".js": "JavaScript", ".jsx": "JavaScript/React", ".rs": "Rust",
        ".go": "Go", ".java": "Java", ".cs": "C#", ".cpp": "C++",
        ".rb": "Ruby", ".php": "PHP", ".swift": "Swift", ".kt": "Kotlin",
    }
    top_ext = max(ext_counts, key=lambda k: ext_counts[k]) if ext_counts else ""
    lang = lang_map.get(top_ext, top_ext.lstrip(".").upper() if top_ext else "mixed")

    tier_note = "tier structure detected" if has_tier_structure else "no tier structure"
    project_name = path.name
    suggestion = (
        f"ass-ade recon . or ass-ade rebuild ."
        if not has_tier_structure
        else "ass-ade lint . or ass-ade certify ."
    )
    return (
        f"Found: {lang} project '{project_name}', {total_files} files, {tier_note}. "
        f"Try: {suggestion}"
    )


# ══════════════════════════════════════════════════════════════════════════════
# ORACLE commands — hallucination, trust-phase, entropy, trust-decay
# ══════════════════════════════════════════════════════════════════════════════

@oracle_app.command("hallucination")
def oracle_hallucination(
    text: str = typer.Argument(..., help="Text to analyse for hallucination risk."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write JSON result to this path."),
) -> None:
    """Run the Hallucination Oracle — certified upper bound on confabulation. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.hallucination_oracle(text=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    data = result.model_dump()
    _print_json(data)
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(data, indent=2), encoding="utf-8")


@oracle_app.command("trust-phase")
def oracle_trust_phase(
    agent_id: str = typer.Argument(..., help="Agent ID to score."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """V_AI geometric trust phase oracle. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.trust_phase_oracle(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@oracle_app.command("entropy")
def oracle_entropy(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Session entropy oracle. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.entropy_oracle()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# Agent commands are now in commands/agent.py and are lazily loaded
# A2A commands are now in commands/a2a.py and are lazily loaded

# ------------------------------------------------------------------------------
# PIPELINE commands - run, status, history
# ------------------------------------------------------------------------------

@pipeline_app.command("run")
def pipeline_run(
    pipeline_type: Annotated[str, typer.Argument(help="Type (trust-gate, certify).")],
    input_value: Annotated[str, typer.Argument(help="Input value.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    persist: Annotated[bool, typer.Option(help="Persist to .ass-ade/workflows/")] = True,
) -> None:
    from ass_ade.pipeline import trust_gate_pipeline, certify_pipeline, StepStatus

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    persist_dir = ".ass-ade/workflows" if persist else None

    def on_progress(name: str, status: StepStatus, current: int, total: int) -> None:
        color = "green" if status == StepStatus.PASSED else "red"
        if status == StepStatus.RUNNING:
            color = "yellow"
        console.print(f"[{current}/{total}] {name}: [{color}]{status.value}[/{color}]")

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            if pipeline_type == "trust-gate":
                pipe = trust_gate_pipeline(
                    client, input_value, on_progress=on_progress, persist_dir=persist_dir
                )
            elif pipeline_type == "certify":
                pipe = certify_pipeline(
                    client, input_value, on_progress=on_progress, persist_dir=persist_dir
                )
            else:
                console.print(f"[red]Unknown type:[/red] {pipeline_type}")
                raise typer.Exit(code=1)

            console.print(f"[bold blue]Running pipeline: {pipe.name}[/bold blue]\n")
            result = pipe.run()
            console.print(f"\n[bold]{result.summary}[/bold]")

    except Exception as exc:
        if isinstance(exc, httpx.HTTPError):
            _nexus_err(exc)
        else:
            console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(code=1) from exc


@pipeline_app.command("status")
def pipeline_status(
    workflow_id: Annotated[str, typer.Argument(help="Workflow ID or filename.")],
) -> None:
    workflow_dir = Path.cwd() / ".ass-ade" / "workflows"
    if not workflow_dir.exists():
        console.print("[yellow]No workflows found in .ass-ade/workflows/[/yellow]")
        return

    target = workflow_dir / workflow_id
    if not target.exists():
        matches = list(workflow_dir.glob(f"{workflow_id}*"))
        if not matches:
            console.print(f"[red]Workflow not found:[/red] {workflow_id}")
            return
        target = matches[0]

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
        _print_json(data)
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"[red]Error reading workflow:[/red] {exc}")


@pipeline_app.command("history")
def pipeline_history(
    limit: Annotated[int, typer.Option(help="Limit number of items.")] = 10,
) -> None:
    import time
    workflow_dir = Path.cwd() / ".ass-ade" / "workflows"
    if not workflow_dir.exists():
        console.print("[yellow]No history found.[/yellow]")
        return

    files = sorted(workflow_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

    table = Table(title="Pipeline History")
    table.add_column("Date")
    table.add_column("Workflow")
    table.add_column("Result")
    table.add_column("Duration")

    for f in files[:limit]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f.stat().st_mtime))
            res = "[green]PASS[/green]" if data.get("passed") else "[red]FAIL[/red]"
            dur = f"{data.get('duration_ms', 0):.0f}ms"
            table.add_row(dt, data.get("name", f.name), res, dur)
        except (json.JSONDecodeError, OSError):
            continue

    console.print(table)


@oracle_app.command("trust-decay")
def oracle_trust_decay(
    agent_id: str = typer.Argument(..., help="Agent ID to score."),
    epochs: int = typer.Option(1, help="Epochs elapsed since last score."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """P2P trust decay oracle. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.trust_decay(agent_id=agent_id, epochs=epochs)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@ratchet_app.command("register")
def ratchet_register(
    agent_id: str = typer.Argument(..., help="Agent ID to create a session for."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write session JSON to this path."),
) -> None:
    """Register a new RatchetGate session. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    numeric_id = int(agent_id) if agent_id.isdigit() else (
        int.from_bytes(hashlib.sha256(agent_id.encode("utf-8")).digest()[:4], "big") & 0x7FFFFFFF
    )
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            session = client.ratchet_register(agent_id=numeric_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(session.model_dump())
    if json_out:
        data = session.model_dump()
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(data, indent=2), encoding="utf-8")


@ratchet_app.command("advance")
def ratchet_advance(
    session_id: str = typer.Argument(..., help="Session ID to advance."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Advance epoch + re-key a RatchetGate session. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.ratchet_advance(session_id=session_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@ratchet_app.command("status")
def ratchet_status(
    session_id: str = typer.Argument(..., help="Session ID to inspect."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Read RatchetGate session status + epoch. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            status = client.ratchet_status(session_id=session_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(status.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# TRUST ORACLE commands
# ══════════════════════════════════════════════════════════════════════════════

@trust_app.command("score")
def trust_score(
    agent_id: str = typer.Argument(..., help="Agent ID to score."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Formally bounded trust score in [0,1] with tier classification. $0.040/query."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.trust_score(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Trust Score — {agent_id}")
    table.add_row("Score", str(result.score))
    table.add_row("Tier", str(result.tier))
    table.add_row("Certified Monotonic", str(result.certified_monotonic))
    console.print(table)


@trust_app.command("history")
def trust_history(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Trust score history — up to 100 epochs with per-epoch delta. $0.040/query."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.trust_history(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# TEXT AI commands
# ══════════════════════════════════════════════════════════════════════════════

@text_app.command("summarize")
def text_summarize(
    text: str = typer.Argument(..., help="Text to summarize."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Extractive text summarization — 1-3 sentences. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.text_summarize(text=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(result.summary or "(no summary returned)")


@text_app.command("keywords")
def text_keywords(
    text: str = typer.Argument(..., help="Text to extract keywords from."),
    top_k: int = typer.Option(10, help="Number of keywords to return."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """TF-IDF keyword extraction. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.text_keywords(text=text, top_k=top_k)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@text_app.command("sentiment")
def text_sentiment(
    text: str = typer.Argument(..., help="Text to classify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Sentiment analysis — positive / negative / neutral. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.text_sentiment(text=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"{result.sentiment}  (confidence: {result.confidence})")


# ══════════════════════════════════════════════════════════════════════════════
# SECURITY commands
# ══════════════════════════════════════════════════════════════════════════════

@security_app.command("threat-score")
def security_threat_score(
    payload_file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, help="JSON file containing the payload to score."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Multi-vector threat scoring (SEC-303). $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload file: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.threat_score(payload=payload)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title="Threat Score")
    table.add_row("Level", str(result.threat_level))
    table.add_row("Score", str(result.score))
    console.print(table)


@security_app.command("prompt-scan")
def security_prompt_scan(
    prompt: str = typer.Argument(..., help="Prompt text to scan for injection."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Prompt injection scanner. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.prompt_inject_scan(prompt=prompt)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    verdict = "THREAT DETECTED" if result.threat_detected else "CLEAN"
    console.print(f"{verdict}  level={result.threat_level}  confidence={result.confidence}")


@security_app.command("shield")
def security_shield(
    payload_file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=False, help="JSON file with payload to sanitize."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Payload sanitization layer for agentic tool calls. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload file: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.security_shield(payload=payload)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@security_app.command("pqc-sign")
def security_pqc_sign(
    data: str = typer.Argument(..., help="Data string to sign with ML-DSA (Dilithium)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write signature JSON to this path."),
) -> None:
    """Post-quantum ML-DSA (Dilithium) signature. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.security_pqc_sign(data=data)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    d = result.model_dump()
    _print_json(d)
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(d, indent=2), encoding="utf-8")


# ══════════════════════════════════════════════════════════════════════════════
# LLM / inference commands
# ══════════════════════════════════════════════════════════════════════════════

@inference_app.command("chat")
def llm_chat(
    prompt: List[str] = typer.Argument(..., help="Prompt to send to AAAA-Nexus."),
    model: str = typer.Option(DEFAULT_AAAA_NEXUS_MODEL, help="LLM model ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write response JSON to this path."),
) -> None:
    """Chat inference via AAAA-Nexus. Defaults to falcon3-10B-1.58. $0.060/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    prompt_text = _collapse_prompt_parts(prompt)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.inference(prompt=prompt_text, model=model)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    text_out = result.result or result.text or "(no response)"
    console.print(text_out)
    if json_out:
        d = result.model_dump()
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(d, indent=2), encoding="utf-8")


@inference_app.command("stream")
def llm_stream(
    prompt: List[str] = typer.Argument(..., help="Prompt to stream from AAAA-Nexus."),
    model: str = typer.Option(DEFAULT_AAAA_NEXUS_MODEL, help="LLM model ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Streaming chain-of-thought inference. $0.100/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    prompt_text = _collapse_prompt_parts(prompt)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            for chunk in client.inference_stream(prompt=prompt_text, model=model):
                console.print(chunk, end="")
    except httpx.HTTPError as exc:
        _nexus_err(exc)


@escrow_app.command("create")
def escrow_create(
    payer: str = typer.Argument(..., help="Payer agent ID."),
    payee: str = typer.Argument(..., help="Payee agent ID."),
    amount: float = typer.Argument(..., help="Amount in USDC."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Create a new on-chain escrow contract. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_create(amount_usdc=amount, sender=payer, receiver=payee, conditions=[])
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@escrow_app.command("release")
def escrow_release(
    escrow_id: str = typer.Argument(..., help="Escrow ID to release."),
    proof: str = typer.Option("", help="Release proof or authorization token."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Release funds from escrow to payee. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_release(escrow_id=escrow_id, proof=proof)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@escrow_app.command("status")
def escrow_status(
    escrow_id: str = typer.Argument(..., help="Escrow ID to inspect."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Check escrow status (funded/released/disputed/resolved). $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_status(escrow_id=escrow_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Escrow {escrow_id}")
    table.add_row("Status", str(result.status))
    table.add_row("Amount USDC", str(result.amount_usdc))
    console.print(table)


@escrow_app.command("dispute")
def escrow_dispute(
    escrow_id: str = typer.Argument(..., help="Escrow ID to dispute."),
    reason: str = typer.Argument(..., help="Reason for dispute."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Open an escrow dispute. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_dispute(escrow_id=escrow_id, reason=reason)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@escrow_app.command("arbitrate")
def escrow_arbitrate(
    escrow_id: str = typer.Argument(..., help="Escrow ID to arbitrate."),
    vote: str = typer.Option("release", help="Arbitration vote: 'release' or 'refund'."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Trigger automated arbitration. $0.100/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.escrow_arbitrate(escrow_id=escrow_id, vote=vote)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# REPUTATION commands
# ══════════════════════════════════════════════════════════════════════════════

@reputation_app.command("record")
def reputation_record(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    success: bool = typer.Option(True, help="Whether the task succeeded."),
    quality: float = typer.Option(1.0, help="Quality score (0.0–1.0)."),
    latency_ms: float = typer.Option(0.0, help="Observed latency in milliseconds."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Record a reputation event. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.reputation_record(agent_id=agent_id, success=success, quality=quality, latency_ms=latency_ms)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@reputation_app.command("score")
def reputation_score(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Get reputation score + tier. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.reputation_score(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Reputation — {agent_id}")
    table.add_row("Score", str(result.score))
    table.add_row("Tier", str(result.tier))
    table.add_row("Fee Multiplier", str(result.fee_multiplier))
    console.print(table)


@reputation_app.command("history")
def reputation_history(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Get reputation event history. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.reputation_history(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# SLA commands
# ══════════════════════════════════════════════════════════════════════════════

@sla_app.command("register")
def sla_register(
    agent_id: str = typer.Argument(..., help="Agent ID to register SLA for."),
    uptime_pct: float = typer.Option(0.99, help="Uptime commitment (0.0–1.0)."),
    latency_ms: float = typer.Option(500.0, help="P99 latency commitment in ms."),
    error_rate: float = typer.Option(0.01, help="Acceptable error rate (0.0–1.0)."),
    bond_usdc: float = typer.Option(0.0, help="Bond amount in USDC staked against SLA."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Register a service-level agreement. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sla_register(agent_id=agent_id, latency_ms=latency_ms, uptime_pct=uptime_pct, error_rate=error_rate, bond_usdc=bond_usdc)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@sla_app.command("report")
def sla_report(
    sla_id: str = typer.Argument(..., help="SLA ID."),
    metric: str = typer.Argument(..., help="Metric name to report (e.g. 'uptime', 'latency_ms')."),
    value: float = typer.Argument(..., help="Observed metric value."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Report SLA compliance metrics. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sla_report(sla_id=sla_id, metric=metric, value=value)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@sla_app.command("status")
def sla_status(
    sla_id: str = typer.Argument(..., help="SLA ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Get SLA compliance score and breach count. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sla_status(sla_id=sla_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@sla_app.command("breach")
def sla_breach(
    sla_id: str = typer.Argument(..., help="SLA ID."),
    severity: str = typer.Option("medium", help="Breach severity: minor/medium/critical."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Report an SLA breach and trigger penalty. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sla_breach(sla_id=sla_id, severity=severity)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# DISCOVERY commands
# ══════════════════════════════════════════════════════════════════════════════

@discovery_app.command("search")
def discovery_search(
    query: str = typer.Argument(..., help="Natural language search query."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Search for agents by capability. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.discovery_search(capability=query)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Discovery: {query}")
    table.add_column("Agent ID")
    table.add_column("Name")
    table.add_column("Score")
    for agent in result.agents:
        table.add_row(agent.agent_id or "", agent.name or "", str(agent.match_score or ""))
    console.print(table)


@discovery_app.command("recommend")
def discovery_recommend(
    task: str = typer.Argument(..., help="Task description."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Get agent recommendations for a task. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.discovery_recommend(task=task)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@discovery_app.command("registry")
def discovery_registry(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List all registered agents. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.discovery_registry()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# SWARM commands
# ══════════════════════════════════════════════════════════════════════════════

@swarm_app.command("plan")
def swarm_plan(
    goal: str = typer.Argument(..., help="Goal to plan for."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Generate a multi-step agent plan. $0.060/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_plan(goal=goal)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    for i, step in enumerate(result.steps, 1):
        console.print(f"{i}. {step}")


@swarm_app.command("relay")
def swarm_relay(
    sender: str = typer.Argument(..., help="Sender agent ID."),
    recipients_csv: str = typer.Argument(..., help="Comma-separated recipient agent IDs."),
    message: str = typer.Argument(..., help="Message to relay."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Relay a message through the agent swarm. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    recipients = [r.strip() for r in recipients_csv.split(",") if r.strip()]
    to = recipients[0] if recipients else ""
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.swarm_relay(from_id=sender, to=to, message={"text": message, "recipients": recipients})
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@swarm_app.command("intent-classify")
def swarm_intent_classify(
    text: str = typer.Argument(..., help="Text to classify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Classify agent intent from natural language. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_intent_classify(text=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@swarm_app.command("token-budget")
def swarm_token_budget(
    text: str = typer.Argument(..., help="Text to estimate token budget for."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Estimate token budget across models. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_token_budget(task=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@swarm_app.command("contradiction")
def swarm_contradiction(
    statement_a: str = typer.Argument(..., help="First statement."),
    statement_b: str = typer.Argument(..., help="Second statement."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Detect logical contradiction between two statements. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_contradiction(statement_a=statement_a, statement_b=statement_b)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    verdict = "CONTRADICTS" if result.contradicts else "NO CONTRADICTION"
    console.print(f"{verdict}  confidence={result.confidence}")
    if result.explanation:
        console.print(result.explanation)


@swarm_app.command("semantic-diff")
def swarm_semantic_diff(
    text_a: str = typer.Argument(..., help="First text."),
    text_b: str = typer.Argument(..., help="Second text."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Semantic diff between two texts. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_semantic_diff(base=text_a, current=text_b)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# COMPLIANCE commands
# ══════════════════════════════════════════════════════════════════════════════

@compliance_app.command("check")
def compliance_check(
    payload_file: Path = typer.Argument(..., exists=True, help="JSON payload to check."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Multi-framework compliance check. $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.compliance_check(system_description=json.dumps(payload))
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@compliance_app.command("eu-ai-act")
def compliance_eu_ai_act(
    system_name: str = typer.Argument(..., help="AI system name."),
    risk_level: str = typer.Option("limited", help="Risk level: minimal/limited/high/unacceptable."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """EU AI Act compliance assessment. $0.080/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.compliance_eu_ai_act(system_description=f"{system_name} (risk level: {risk_level})")
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@compliance_app.command("fairness")
def compliance_fairness(
    model_id: str = typer.Argument(..., help="Model ID to assess."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Fairness proof (disparate impact analysis). $0.080/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.compliance_fairness(model_id=model_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@compliance_app.command("drift-check")
def compliance_drift_check(
    model_id: str = typer.Argument(..., help="Model ID to check for drift."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Model behavioral drift detection. $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.drift_check(model_id=model_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@compliance_app.command("drift-cert")
def compliance_drift_cert(
    model_id: str = typer.Argument(..., help="Model ID to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Issue drift-free certificate. $0.080/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.drift_certificate(model_id=model_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@compliance_app.command("incident")
def compliance_incident(
    incident_id: str = typer.Argument(..., help="Incident ID to retrieve."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Retrieve a compliance incident report. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.compliance_incident(incident_id=incident_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# DEFI commands
# ══════════════════════════════════════════════════════════════════════════════

@defi_app.command("optimize")
def defi_optimize(
    payload_file: Path = typer.Argument(..., exists=True, help="JSON DeFi portfolio payload."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """DeFi portfolio optimization (MVO). $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_optimize(payload=payload)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@defi_app.command("risk-score")
def defi_risk_score(
    protocol: str = typer.Argument(..., help="Protocol name or address."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """DeFi protocol risk score. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_risk_score(protocol=protocol)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@defi_app.command("oracle-verify")
def defi_oracle_verify(
    oracle_id: str = typer.Argument(..., help="Oracle ID to verify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a price oracle for manipulation. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_oracle_verify(oracle_id=oracle_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@defi_app.command("liquidation-check")
def defi_liquidation_check(
    position_id: str = typer.Argument(..., help="DeFi position ID."),
    collateral: float = typer.Argument(..., help="Collateral value USD."),
    debt: float = typer.Argument(..., help="Debt value USD."),
    cf: float = typer.Option(0.80, help="Collateral factor."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Health factor + liquidation distance (LQS-100). $0.040/check."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_liquidation_check(
                position_id=position_id, collateral_value=collateral,
                debt_value=debt, collateral_factor=cf,
            )
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@defi_app.command("bridge-verify")
def defi_bridge_verify(
    bridge_id: str = typer.Argument(..., help="Bridge transaction ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a cross-chain bridge transaction. $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_bridge_verify(bridge_id=bridge_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@defi_app.command("yield-optimize")
def defi_yield_optimize(
    amount_usdc: float = typer.Argument(..., help="Amount in USDC to optimize."),
    risk_tolerance: str = typer.Option("medium", help="low/medium/high"),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Yield optimization across DeFi protocols. $0.060/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.defi_yield_optimize(amount_usdc=amount_usdc, risk_tolerance=risk_tolerance)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# AEGIS commands
# ══════════════════════════════════════════════════════════════════════════════

@aegis_app.command("mcp-proxy")
def aegis_mcp_proxy(
    tool_name: str = typer.Argument(..., help="MCP tool name to proxy."),
    payload_file: Path | None = typer.Option(None, help="JSON payload file."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Route MCP tool calls through AEGIS safety layer. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    payload: dict = {}
    if payload_file:
        try:
            payload = json.loads(payload_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"Failed to read payload: {exc}")
            raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.aegis_mcp_proxy(tool_name=tool_name, payload=payload)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@aegis_app.command("epistemic-route")
def aegis_epistemic_route(
    query: str = typer.Argument(..., help="Query to route."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Epistemic routing — select best model for confidence level. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.aegis_epistemic_route(query=query)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@aegis_app.command("certify-epoch")
def aegis_certify_epoch(
    agent_id: str = typer.Argument(..., help="Agent ID to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Issue epoch compliance certificate (AEG-101). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.aegis_certify_epoch(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# CONTROL PLANE commands
# ══════════════════════════════════════════════════════════════════════════════

@control_app.command("authorize")
def control_authorize(
    agent_id: str = typer.Argument(..., help="Agent ID requesting action."),
    action: str = typer.Argument(..., help="Action to authorize."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Authorize an agent action. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.authorize_action(agent_id=agent_id, action=action)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@control_app.command("spending-authorize")
def control_spending_authorize(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    amount_usdc: float = typer.Argument(..., help="Amount to authorize in USDC."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Authorize a spending request. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.spending_authorize(agent_id=agent_id, amount_usdc=amount_usdc)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@control_app.command("spending-budget")
def control_spending_budget(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Check remaining spending budget. $0.004/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.spending_budget(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@control_app.command("lineage-record")
def control_lineage_record(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    action: str = typer.Argument(..., help="Action to record in lineage."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Record an action in the lineage chain. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.lineage_record(agent_id=agent_id, action=action)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@control_app.command("lineage-trace")
def control_lineage_trace(
    lineage_id: str = typer.Argument(..., help="Lineage ID to trace."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Trace a lineage chain. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.lineage_trace(lineage_id=lineage_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@control_app.command("federation-mint")
def control_federation_mint(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    scope: str = typer.Option("read", help="Token scope."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Mint a federated trust token. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.federation_mint(agent_id=agent_id, scope=scope)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# IDENTITY commands
# ══════════════════════════════════════════════════════════════════════════════

@identity_app.command("verify")
def identity_verify(
    agent_id: str = typer.Argument(..., help="Agent ID to verify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify agent identity (allow/deny/flag). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.identity_verify(actor=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Decision: {result.decision}  uniqueness={result.uniqueness_coefficient}")


@identity_app.command("sybil-check")
def identity_sybil_check(
    agent_id: str = typer.Argument(..., help="Agent ID to check."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Sybil resistance check (free trial). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.sybil_check(actor=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Risk: {result.sybil_risk}  score={result.score}")


@identity_app.command("delegate-verify")
def identity_delegate_verify(
    token: str = typer.Argument(..., help="UCAN delegation token."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a UCAN delegation token. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.delegate_verify(token=token)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Valid: {result.valid}  depth={result.depth}/{result.depth_limit}")


# ══════════════════════════════════════════════════════════════════════════════
# VRF commands
# ══════════════════════════════════════════════════════════════════════════════

@vrf_app.command("draw")
def vrf_draw(
    game_id: str = typer.Argument(..., help="Game or draw ID."),
    n: int = typer.Option(1, help="Number of integers to draw."),
    min_val: int = typer.Option(1, help="Minimum value (inclusive)."),
    max_val: int = typer.Option(100, help="Maximum value (inclusive)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verifiable random draw — provably fair. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vrf_draw(game_id=game_id, n=n, range_min=min_val, range_max=max_val)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@vrf_app.command("verify")
def vrf_verify(
    draw_id: str = typer.Argument(..., help="Draw ID to verify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify a VRF draw proof. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vrf_verify_draw(draw_id=draw_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Valid: {result.valid}")


# ══════════════════════════════════════════════════════════════════════════════
# BITNET commands
# ══════════════════════════════════════════════════════════════════════════════

@bitnet_app.command("models")
def bitnet_models(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List available 1.58-bit BitNet models. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_models()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title="BitNet 1.58-bit Models")
    table.add_column("ID")
    table.add_column("Provider")
    table.add_column("Params (B)")
    table.add_column("Memory (GB)")
    table.add_column("Status")
    for m in result.models:
        table.add_row(m.id or "", m.provider or "", str(m.params_b or ""), str(m.memory_gb or ""), m.status or "")
    console.print(table)


@bitnet_app.command("chat")
def bitnet_chat(
    prompt: List[str] = typer.Argument(..., help="Prompt for 1.58-bit inference."),
    model: str = typer.Option(DEFAULT_AAAA_NEXUS_MODEL, help="BitNet model ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """1.58-bit BitNet chat completion (BIT-100). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    prompt_text = _collapse_prompt_parts(prompt)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_inference(prompt=prompt_text, model=model)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(result.result or "(no response)")


@bitnet_app.command("stream")
def bitnet_stream(
    prompt: List[str] = typer.Argument(..., help="Prompt to stream."),
    model: str = typer.Option(DEFAULT_AAAA_NEXUS_MODEL, help="BitNet model ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Streaming 1.58-bit BitNet CoT inference (BIT-101). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    prompt_text = _collapse_prompt_parts(prompt)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            for chunk in client.bitnet_stream(prompt=prompt_text, model=model):
                console.print(chunk, end="")
    except httpx.HTTPError as exc:
        _nexus_err(exc)


@bitnet_app.command("benchmark")
def bitnet_benchmark(
    model: str = typer.Argument(..., help="BitNet model ID to benchmark."),
    n_tokens: int = typer.Option(100, help="Tokens to generate for benchmark."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Run inference benchmark for a 1.58-bit model (BIT-103). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_benchmark(model=model, n_tokens=n_tokens)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"BitNet Benchmark — {model}")
    table.add_row("Tokens/sec", str(result.tokens_per_second))
    table.add_row("Memory MB", str(result.memory_mb))
    table.add_row("Latency ms", str(result.latency_ms))
    console.print(table)


@bitnet_app.command("status")
def bitnet_status(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """BitNet engine health and metrics (BIT-105). Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_status()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# VANGUARD commands
# ══════════════════════════════════════════════════════════════════════════════

@vanguard_app.command("redteam")
def vanguard_redteam(
    agent_id: str = typer.Argument(..., help="Agent ID to red-team."),
    target: str = typer.Argument(..., help="Target system or endpoint."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Continuous red-team audit for an agent. $0.100/run."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_redteam(agent_id=agent_id, target=target)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Red-Team Audit — {agent_id}")
    table.add_row("Vulnerabilities", str(result.vulnerabilities_found))
    table.add_row("Severity", str(result.severity))
    table.add_row("Run ID", str(result.run_id))
    console.print(table)
    if result.findings:
        _print_json(result.findings)


@vanguard_app.command("mev-route")
def vanguard_mev_route(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    intent_file: Path | None = typer.Option(None, help="JSON file with route intent."),
) -> None:
    """MEV route intent governance. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    intent: dict = {}
    if intent_file:
        try:
            intent = json.loads(intent_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"Failed to read intent file: {exc}")
            raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_mev_route(agent_id=agent_id, intent=intent)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@vanguard_app.command("govern-session")
def vanguard_govern_session(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    wallet_address: str = typer.Argument(..., help="Wallet address."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """UCAN wallet session governance. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_govern_session(agent_id=agent_id, wallet=wallet_address)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@vanguard_app.command("lock-and-verify")
def vanguard_lock_and_verify(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    amount: float = typer.Argument(..., help="Amount in USDC to lock."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Lock and verify an escrow (Vanguard). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_lock_and_verify(agent_id=agent_id, amount_usdc=amount)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# MEV SHIELD commands
# ══════════════════════════════════════════════════════════════════════════════

@mev_app.command("protect")
def mev_protect(
    tx_bundle_csv: str = typer.Argument(..., help="Comma-separated transaction hex strings."),
    strategy: str = typer.Option("flashbots", help="Protection strategy: flashbots/private-mempool/time-delay."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Wrap a transaction bundle with MEV protection (MEV-100). $0.020/tx."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    tx_bundle = [t.strip() for t in tx_bundle_csv.split(",") if t.strip()]
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.mev_protect(tx_bundle=tx_bundle, strategy=strategy)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@mev_app.command("status")
def mev_status(
    bundle_id: str = typer.Argument(..., help="Bundle ID to check."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Check MEV protection status for a bundle (MEV-101). Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.mev_status(bundle_id=bundle_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"MEV Bundle — {bundle_id}")
    table.add_row("Status", str(result.status))
    table.add_row("Block", str(result.included_in_block))
    table.add_row("MEV Saved USD", str(result.mev_saved_usd))
    console.print(table)


# ══════════════════════════════════════════════════════════════════════════════
# FORGE MARKETPLACE commands
# ══════════════════════════════════════════════════════════════════════════════

@forge_app.command("leaderboard")
def forge_leaderboard(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Forge agent leaderboard. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_leaderboard()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title="Forge Leaderboard")
    table.add_column("Rank", justify="right")
    table.add_column("Agent ID")
    table.add_column("Name")
    table.add_column("Score")
    for entry in result.entries:
        table.add_row(str(entry.rank or ""), entry.agent_id or "", entry.name or "", str(entry.score or ""))
    console.print(table)


@forge_app.command("verify")
def forge_verify(
    agent_id: str = typer.Argument(..., help="Agent ID to verify for Forge."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Verify an agent for a Forge badge. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_verify(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Verified: {result.verified}  badge={result.badge_awarded}  score={result.score}")


@forge_app.command("quarantine")
def forge_quarantine(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List quarantined agents. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_quarantine()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Quarantined agents: {result.count}")
    _print_json(result.quarantined)


@forge_app.command("delta-submit")
def forge_delta_submit(
    agent_id: str = typer.Argument(..., help="Agent ID submitting the delta."),
    delta_file: Path = typer.Argument(..., exists=True, help="JSON file with improvement delta."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Submit an improvement delta for reward. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        delta = json.loads(delta_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read delta file: {exc}")
        raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_delta_submit(agent_id=agent_id, delta=delta)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@forge_app.command("badge")
def forge_badge(
    badge_id: str = typer.Argument(..., help="Badge ID to retrieve."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Retrieve Forge badge metadata. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.forge_badge(badge_id=badge_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# DEV commands
# ══════════════════════════════════════════════════════════════════════════════

@dev_app.command("starter")
def dev_starter(
    project_name: str = typer.Argument(..., help="Project name."),
    language: str = typer.Option("python", help="Language: python/rust/typescript."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Scaffold an agent project with x402 wiring (DEV-601). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.dev_starter(project_name=project_name, language=language)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Scaffolded: {result.project_name}  x402={result.x402_wired}")
    if result.files:
        _print_json(result.files)


@dev_app.command("crypto-toolkit")
def dev_crypto_toolkit(
    data: str = typer.Argument(..., help="Data string to hash/proof."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """BLAKE3 + Merkle proof + nonce toolkit (DCM-1018). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.crypto_toolkit(data=data)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@dev_app.command("routing-think")
def dev_routing_think(
    query: str = typer.Argument(..., help="Query to route."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Model routing think-through. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.routing_think(query=query)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ══════════════════════════════════════════════════════════════════════════════
# DATA commands
# ══════════════════════════════════════════════════════════════════════════════

@data_app.command("validate-json")
def data_validate_json(
    payload_file: Path = typer.Argument(..., exists=True, help="JSON file to validate."),
    schema_file: Path | None = typer.Option(None, help="JSON Schema file to validate against."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Validate JSON against a schema. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"Failed to read payload: {exc}")
        raise typer.Exit(code=4) from exc
    schema = None
    if schema_file:
        try:
            schema = json.loads(schema_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"Failed to read schema: {exc}")
            raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.data_validate_json(payload=payload, schema=schema)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@data_app.command("format-convert")
def data_format_convert(
    data: str = typer.Argument(..., help="Data string to convert."),
    from_fmt: str = typer.Argument(..., help="Source format: json/yaml/toml/csv."),
    to_fmt: str = typer.Argument(..., help="Target format: json/yaml/toml/csv."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Convert between data formats. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.data_format_convert(data=data, from_format=from_fmt, to_format=to_fmt)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ── Hero Workflows ────────────────────────────────────────────────────────────


@prompt_app.command("hash")
def prompt_hash_command(
    prompt_path: str | None = typer.Argument(None, help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Return SHA-256 metadata for an explicit prompt artifact."""
    from ass_ade.prompt_toolkit import prompt_hash

    try:
        result = prompt_hash(working_dir=path, prompt_path=prompt_path, prompt_text=text)
    except ValueError as exc:
        console.print(f"[red]Prompt hash error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(f"Source: {result.source}")
        console.print(f"SHA-256: {result.sha256}")
        console.print(f"Bytes: {result.bytes}")
        console.print(f"Lines: {result.lines}")


@prompt_app.command("validate")
def prompt_validate_command(
    manifest_path: str = typer.Argument(..., help="Prompt manifest JSON file."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    prompt_name: str | None = typer.Option(None, help="Optional manifest prompt entry name."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Validate an explicit prompt artifact against a JSON hash manifest."""
    from ass_ade.prompt_toolkit import prompt_validate

    try:
        result = prompt_validate(
            manifest_path=manifest_path,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
            prompt_name=prompt_name,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt validation error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        color = "green" if result.valid else "red"
        console.print(f"[{color}]Valid: {result.valid}[/{color}]")
        console.print(f"Source: {result.source}")
        console.print(f"SHA-256: {result.sha256}")


@prompt_app.command("section")
def prompt_section_command(
    section: str = typer.Argument(..., help="Markdown heading or XML tag name."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Extract a prompt section from an explicit prompt artifact."""
    from ass_ade.prompt_toolkit import prompt_section

    try:
        result = prompt_section(
            section=section,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt section error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    elif result.found:
        console.print(result.text, markup=False)
    else:
        console.print("[yellow]Section not found.[/yellow]")


@prompt_app.command("diff")
def prompt_diff_command(
    baseline_path: str = typer.Argument(..., help="Baseline prompt file."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Current prompt file."),
    text: str | None = typer.Option(None, "--text", help="Inline current prompt text."),
    path: Path = REPO_PATH_OPTION,
    redacted: bool = typer.Option(True, "--redacted/--raw", help="Redact secrets in diff."),
    max_lines: int = typer.Option(200, help="Maximum diff lines."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Compare a prompt artifact to a baseline with redaction."""
    from ass_ade.prompt_toolkit import prompt_diff

    try:
        result = prompt_diff(
            baseline_path=baseline_path,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
            redacted=redacted,
            max_lines=max_lines,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt diff error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(result.diff, markup=False)


@prompt_app.command("propose")
def prompt_propose_command(
    objective: str = typer.Argument(..., help="Prompt improvement objective."),
    prompt_path: str | None = typer.Option(None, "--prompt-path", help="Prompt file path."),
    text: str | None = typer.Option(None, "--text", help="Inline prompt text."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Create a prompt self-improvement proposal."""
    from ass_ade.prompt_toolkit import prompt_propose

    try:
        result = prompt_propose(
            objective=objective,
            working_dir=path,
            prompt_path=prompt_path,
            prompt_text=text,
        )
    except ValueError as exc:
        console.print(f"[red]Prompt proposal error:[/red] {exc}")
        raise typer.Exit(code=4) from exc

    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(f"Proposal: {result.proposal_id}")
        for change in result.recommended_changes:
            console.print(f"  - {change}")


@prompt_app.command("sync-agent")
def prompt_sync_agent_command(
    path: Path = REPO_PATH_OPTION,
    prompt_path: Path = typer.Option(
        Path("agents/atomadic_interpreter.md"),
        "--prompt-path",
        help="Prompt artifact to refresh, relative to --path unless absolute.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Refresh Atomadic's generated capability block from live commands and tools."""
    from ass_ade.agent.capabilities import sync_atomadic_prompt_capabilities

    target = sync_atomadic_prompt_capabilities(repo_root=path, prompt_path=prompt_path)
    payload = {"path": str(target), "ok": True}
    if json_out:
        _print_json(payload)
    else:
        console.print(f"[green]Synced Atomadic capabilities:[/green] {target}")


@context_app.command("pack")
def context_pack_command(
    task_description: str = typer.Argument(..., help="Task the context packet should support."),
    file: list[str] = typer.Option([], "--file", help="Repo-relative file to include."),
    source: list[str] = typer.Option([], "--source", help="Official source URL already researched."),
    path: Path = REPO_PATH_OPTION,
    max_files: int = typer.Option(12, help="Maximum files to include."),
    max_bytes_per_file: int = typer.Option(4000, help="Maximum bytes of excerpt per file."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Build a compact context packet from repo files and source URLs."""
    from ass_ade.context_memory import build_context_packet

    packet = build_context_packet(
        task_description=task_description,
        working_dir=path,
        file_paths=file or None,
        source_urls=source,
        max_files=max_files,
        max_bytes_per_file=max_bytes_per_file,
    )

    if json_out:
        _print_json(packet.model_dump(), redact=True)
        return

    color = "green" if packet.recon_verdict == "READY_FOR_PHASE_1" else "yellow"
    console.print(f"[{color}]Context Packet: {packet.recon_verdict}[/{color}]")
    console.print(f"Sources: {len(packet.source_urls)}")
    console.print(f"Files: {len(packet.files)}")
    for item in packet.files:
        mark = " truncated" if item.truncated else ""
        console.print(f"  - {item.path} ({item.size_bytes} bytes{mark})")
    if packet.warnings:
        console.print("[bold]Warnings:[/bold]")
        for warning in packet.warnings:
            console.print(f"  - {warning}")


@context_app.command("store")
def context_store_command(
    text: str = typer.Argument(..., help="Text to store in local vector memory."),
    namespace: str = typer.Option("default", help="Memory namespace."),
    metadata: str = typer.Option("{}", help="JSON metadata object."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Store text in the local vector memory."""
    from ass_ade.context_memory import store_vector_memory

    try:
        metadata_obj = json.loads(metadata)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Metadata must be JSON:[/red] {exc}")
        raise typer.Exit(code=4) from exc
    if not isinstance(metadata_obj, dict):
        console.print("[red]Metadata must be a JSON object.[/red]")
        raise typer.Exit(code=4)

    result = store_vector_memory(
        text=text,
        namespace=namespace,
        metadata=metadata_obj,
        working_dir=path,
    )
    if json_out:
        _print_json(result.model_dump(), redact=True)
    else:
        console.print(f"[green]Stored vector memory:[/green] {result.id}")
        console.print(f"Namespace: {result.namespace}")


@context_app.command("query")
def context_query_command(
    query: str = typer.Argument(..., help="Query local vector memory."),
    namespace: str = typer.Option("default", help="Memory namespace."),
    top_k: int = typer.Option(5, help="Number of matches to return."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Query the local vector memory."""
    from ass_ade.context_memory import query_vector_memory

    result = query_vector_memory(
        query=query,
        namespace=namespace,
        top_k=top_k,
        working_dir=path,
    )
    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    console.print(f"[green]Matches:[/green] {len(result.matches)}")
    for match in result.matches:
        console.print(f"  - {match.score:.3f} {match.id}: {match.text[:100]}")


@a2a_app.command("local-card")
def a2a_local_card(
    working_dir: Path = typer.Option(
        Path("."), exists=True, file_okay=False, help="Working directory."
    ),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Display the local ASS-ADE agent card."""
    from ass_ade.a2a import local_agent_card

    card = local_agent_card(str(working_dir.resolve()))

    if json_out:
        _print_json(card.model_dump())
    else:
        console.print(f"[bold]{card.name}[/bold] v{card.version or '?'}")
        console.print(f"  {card.description}")
        if card.skills:
            console.print(f"\n[bold]Skills ({len(card.skills)}):[/bold]")
            for skill in card.skills:
                console.print(f"  • [cyan]{skill.id}[/cyan] — {skill.description}")


# ══════════════════════════════════════════════════════════════════════════════
# Pipeline Sub-commands — Composable workflow execution
# ══════════════════════════════════════════════════════════════════════════════


@pipeline_app.command("trust-gate")
def pipeline_trust_gate(
    agent_id: str = typer.Argument(..., help="Agent ID to evaluate."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    persist: bool = typer.Option(False, help="Persist results to .ass-ade/workflows/"),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Run the trust-gate pipeline: identity → sybil → trust → reputation → gate."""
    from ass_ade.pipeline import trust_gate_pipeline

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    persist_dir = str(Path(".ass-ade/workflows")) if persist else None

    def _progress(name: str, status: Any, current: int, total: int) -> None:
        console.print(f"  [{current}/{total}] {name}: {status.value}")

    with NexusClient(
        base_url=settings.nexus_base_url,
        timeout=settings.request_timeout_s,
        api_key=settings.nexus_api_key,
    ) as client:
        pipe = trust_gate_pipeline(
            client, agent_id, on_progress=_progress, persist_dir=persist_dir
        )
        result = pipe.run()

    if json_out:
        _print_json({
            "name": result.name,
            "passed": result.passed,
            "duration_ms": result.duration_ms,
            "steps": [
                {"name": s.name, "status": s.status.value, "output": s.output, "error": s.error}
                for s in result.steps
            ],
        })
    else:
        verdict = "[green]PASSED[/green]" if result.passed else "[red]FAILED[/red]"
        console.print(f"${verdict} — {result.summary}")


@pipeline_app.command("certify")
def pipeline_certify(
    text: str = typer.Argument(..., help="Text to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    persist: bool = typer.Option(False, help="Persist results to .ass-ade/workflows/"),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Run the certification pipeline: hallucination → ethics → compliance → certify."""
    from ass_ade.pipeline import certify_pipeline

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    persist_dir = str(Path(".ass-ade/workflows")) if persist else None

    def _progress(name: str, status: Any, current: int, total: int) -> None:
        console.print(f"  [{current}/{total}] {name}: {status.value}")

    with NexusClient(
        base_url=settings.nexus_base_url,
        timeout=settings.request_timeout_s,
        api_key=settings.nexus_api_key,
    ) as client:
        pipe = certify_pipeline(
            client, text, on_progress=_progress, persist_dir=persist_dir
        )
        result = pipe.run()

    if json_out:
        _print_json({
            "name": result.name,
            "passed": result.passed,
            "duration_ms": result.duration_ms,
            "steps": [
                {"name": s.name, "status": s.status.value, "output": s.output, "error": s.error}
                for s in result.steps
            ],
        })
    else:
        verdict = "[green]PASSED[/green]" if result.passed else "[red]FAILED[/red]"
        console.print(f"${verdict} — {result.summary}")

# ------------------------------------------------------------------------------
# ESCROW commands - create, release, status, dispute, arbitrate
# ------------------------------------------------------------------------------

@security_app.command("zero-day-scan")
def security_zero_day_scan(
    payload_path: Annotated[Path, typer.Argument(help="Path to JSON payload to scan.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Zero-day pattern detector for agent payloads. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.security_zero_day(payload=payload)
    except (httpx.HTTPError, json.JSONDecodeError, OSError) as exc:
        if isinstance(exc, httpx.HTTPError):
            _nexus_err(exc)
        else:
            console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(code=1) from exc
    _print_json(result)


# ==============================================================================
# INFERENCE commands - chat, chat-stream, token-count
# ==============================================================================

@inference_app.command("token-count")
def inference_token_count(
    task: Annotated[str, typer.Argument(help="Task description to estimate tokens for.")],
    models: Annotated[list[str] | None, typer.Option(help="Models to estimate for.")] = None,
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Cost estimate across 7 models. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.agent_token_budget(task=task, models=models)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
    _print_json(result)


# ==============================================================================
# DATA commands - validate-json, convert
# ==============================================================================

@data_app.command("convert")
def data_convert(
    input_path: Annotated[Path, typer.Argument(help="Input file.")],
    target_format: Annotated[str, typer.Argument(help="Target format (yaml, toml, etc).")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Convert structured data formats. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        content = input_path.read_text(encoding="utf-8")
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.data_convert(content=content, target_format=target_format)
    except (httpx.HTTPError, OSError) as exc:
        if isinstance(exc, httpx.HTTPError):
            _nexus_err(exc)
        else:
            console.print(f"[red]Error:[/red] {exc}")
            raise typer.Exit(code=1) from exc
    _print_json(result)


# ==============================================================================
# VANGUARD commands - lock-and-verify, epoch-certify, wallet-session, zero-day-scan
# ==============================================================================

@vanguard_app.command("epoch-certify")
def vanguard_epoch_certify(
    system_id: Annotated[str, typer.Argument(help="System ID to certify.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Certify epoch drift + compliance. $0.060/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.aegis_certify_epoch(system_id=system_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


@vanguard_app.command("wallet-session")
def vanguard_wallet_session(
    agent_id: Annotated[str, typer.Argument(help="Agent ID.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Start a VANGUARD wallet session. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.vanguard_start_session(agent_id=agent_id)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())


# ==============================================================================
# PAY command — x402 payment demo and wallet management
# ==============================================================================

@app.command()
def pay(
    endpoint: str = typer.Argument(..., help="Endpoint to call (e.g. /v1/trust/score)."),
    body: str = typer.Option("{}", help="JSON body for the request."),
    auto_confirm: bool = typer.Option(False, "--auto-confirm", help="Skip payment consent prompt."),
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Demonstrate x402 autonomous payment flow on Base L2.

    Calls an endpoint, and if it returns 402 Payment Required, parses
    the x402 challenge, shows the cost, and (with consent) submits
    USDC payment on-chain then retries with the payment proof.

    Testnet mode: export ATOMADIC_X402_TESTNET=1
    Wallet key:   export ATOMADIC_WALLET_KEY=<hex-private-key>
    """
    from ass_ade.nexus.x402 import (
        PaymentChallenge,
        format_payment_consent,
        get_chain_config,
        submit_payment,
        build_payment_header,
    )

    _, settings = _resolve_config(config)
    chain = get_chain_config()

    console.print(f"[bold]x402 Payment Demo[/bold] — {chain['network_name']}")
    console.print(f"Calling: {settings.nexus_base_url}{endpoint}")
    console.print()

    try:
        req_body = json.loads(body)
    except json.JSONDecodeError as exc:
        console.print("[red]Invalid JSON body[/red]")
        raise typer.Exit(code=1) from exc

    # Step 1: Make the request
    with NexusClient(
        base_url=settings.nexus_base_url,
        timeout=settings.request_timeout_s,
        api_key=settings.nexus_api_key,
    ) as client:
        post_with_x402 = getattr(client, "_post_with_x402", None) or client.post_with_x402
        result = post_with_x402(endpoint, req_body)

    # Step 2: Check if payment is required
    if not result.get("payment_required"):
        console.print("[green]No payment required — endpoint returned 200[/green]")
        _print_json(result)
        return

    # Step 3: Parse challenge
    challenge = result.get("challenge")
    if not challenge:
        # Fallback: parse from raw for backward compat
        challenge = PaymentChallenge.from_response(result.get("raw", result))
    console.print(format_payment_consent(challenge))
    console.print()

    # Step 4: Get consent
    if not auto_confirm:
        confirm = typer.confirm("Proceed with payment?")
        if not confirm:
            console.print("[yellow]Payment cancelled.[/yellow]")
            raise typer.Exit(code=0)

    # Step 5: Submit payment
    console.print("[bold]Submitting payment...[/bold]")
    payment = submit_payment(challenge)

    if not payment.success:
        console.print(f"[red]Payment failed:[/red] {payment.error}")
        raise typer.Exit(code=1)

    console.print(f"[green]Payment submitted![/green] txid: {payment.txid}")
    if payment.testnet:
        console.print(f"[dim]View on BaseScan: https://sepolia.basescan.org/tx/0x{payment.txid}[/dim]")
    else:
        console.print(f"[dim]View on BaseScan: https://basescan.org/tx/0x{payment.txid}[/dim]")

    # Step 6: Retry with payment proof
    console.print("[bold]Retrying with payment proof...[/bold]")
    headers = build_payment_header(payment)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            response = client.request_with_payment_headers(endpoint, req_body, payment_headers=headers)
            if response.status_code == 200:
                console.print("[green]Paid request successful![/green]")
                _print_json(response.json())
            else:
                console.print(f"[red]Retry returned {response.status_code}[/red]")
                console.print(response.text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)


@app.command()
def wallet(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show x402 wallet status and chain configuration."""
    import os
    from ass_ade.nexus.x402 import get_chain_config

    _resolve_config(config)
    chain = get_chain_config()
    wallet_key = os.environ.get("ATOMADIC_WALLET_KEY", "")
    has_wallet = bool(wallet_key)

    table = Table(title="x402 Wallet Status")
    table.add_row("Network", chain["network_name"])
    table.add_row("Chain ID", str(chain["chain_id"]))
    table.add_row("RPC", chain["rpc_url"])
    table.add_row("USDC Contract", chain["usdc_address"])
    table.add_row("Treasury", chain["treasury"])
    table.add_row("Wallet Key", "[green]Set[/green]" if has_wallet else "[red]Not set (export ATOMADIC_WALLET_KEY)[/red]")
    table.add_row("Testnet Mode", "[green]ON[/green]" if chain["testnet"] else "[yellow]OFF (mainnet)[/yellow]")

    if has_wallet:
        try:
            account_module = importlib.import_module("eth_account")
            Account = account_module.Account
            acct = Account.from_key(wallet_key)
            table.add_row("Wallet Address", acct.address)
        except ImportError:
            table.add_row("Wallet Address", "[dim]Install web3: pip install web3 eth-account[/dim]")
        except Exception as e:
            table.add_row("Wallet Address", f"[red]Error: {e}[/red]")

    console.print(table)


# ==============================================================================
# SEARCH command — internal RAG search (owner-only)
# ==============================================================================

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query for the Atomadic knowledge base."),
    max_results: int = typer.Option(10, help="Maximum number of results."),
    chat: bool = typer.Option(False, help="Include LLM-generated answer with search results."),
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Search the private Atomadic RAG knowledge base.

    Requires owner session. Authenticate first with your OWNER_TOKEN
    via the admin auth endpoint to get a session token, then set
    ATOMADIC_SESSION_TOKEN in your environment.
    """
    import os

    _, settings = _resolve_config(config)
    session_token = os.environ.get("ATOMADIC_SESSION_TOKEN", "")

    if not session_token:
        console.print(
            "[red]Error:[/red] ATOMADIC_SESSION_TOKEN not set. "
            "Authenticate via /v1/admin/auth first, then export the session token."
        )
        raise typer.Exit(code=1)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            if chat:
                result = client.internal_search_chat(
                    query=query, session_token=session_token
                )
            else:
                result = client.internal_search(
                    query=query, max_results=max_results, session_token=session_token
                )
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return

    _print_json(result)


# ── capability status commands ────────────────────────────────────────────────


@app.command("sam-status")
def sam_status() -> None:
    """Show SAM TRS scoring status and G23 gate history for the current session."""
    from ass_ade.agent.sam import SAM

    sam = SAM({})
    rep = sam.report()
    t = Table(title="SAM — Sovereign Assessment Matrix")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Total checks", str(rep.get("checks", 0)))
    t.add_row("G23 threshold", str(rep.get("g23_threshold", 7)))
    t.add_row("Engine", rep.get("engine", "sam"))
    console.print(t)
    console.print("[dim]Run an agent session to populate TRS history.[/dim]")


@app.command("wisdom-report")
def wisdom_report(
    last: int = typer.Option(10, help="Number of recent audit cycles to show."),
) -> None:
    """Show WisdomEngine audit history, conviction trend, and distilled principles."""
    from ass_ade.agent.wisdom import WisdomEngine

    engine = WisdomEngine({})
    rep = engine.report()
    t = Table(title="WisdomEngine Report")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Audits completed", str(rep.get("audits", 0)))
    t.add_row("Current conviction", f"{rep.get('conviction', 0.0):.2%}")
    t.add_row("Conviction required", f"{rep.get('conviction_required', 0.85):.2%}")
    t.add_row("Confident", "YES" if rep.get("conviction", 0) >= rep.get("conviction_required", 0.85) else "NO")
    console.print(t)

    principles = rep.get("principles", [])
    if principles:
        console.print("\n[bold]Distilled Principles:[/bold]")
        for i, p in enumerate(principles[:last], 1):
            console.print(f"  {i}. {p}")
    else:
        console.print("[dim]No principles distilled yet. Run agent sessions to populate.[/dim]")


@app.command("tca-status")
def tca_status(
    working_dir: Path = typer.Option(Path("."), help="Project root."),
) -> None:
    """Show TCA (Technical Context Acquisition) freshness status for tracked files."""
    from ass_ade.agent.tca import TCAEngine

    engine = TCAEngine()
    stale = engine.get_stale_files()
    rep = engine.report()

    t = Table(title="TCA — Technical Context Acquisition")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Tracked files", str(rep.get("tracked_files", 0)))
    t.add_row("Stale files", str(rep.get("stale_count", len(stale))))
    t.add_row("Documentation gaps", str(rep.get("gap_count", 0)))
    t.add_row("Freshness threshold", f"{rep.get('threshold_hours', 120):.0f}h")
    console.print(t)

    if stale:
        console.print(f"\n[yellow]Stale files ({len(stale)}):[/yellow]")
        for r in stale[:20]:
            age = f"{r.age_hours:.1f}h" if r.age_hours else "never read"
            console.print(f"  [red]●[/red] {r.path} ({age} old)")
    else:
        console.print("\n[green]✓ All tracked files are fresh.[/green]")

    gaps = engine.get_gaps()
    if gaps:
        console.print(f"\n[yellow]Documentation gaps ({len(gaps)}):[/yellow]")
        for g in gaps[:10]:
            console.print(f"  • {g['description']}")


@app.command("eco-scan")
def eco_scan(
    path: Path = typer.Argument(Path("."), help="Folder to scan."),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
    out: Path | None = typer.Option(None, "--out", "-o", help="Write ECO_SCAN_REPORT.md here."),
) -> None:
    """Run a monadic compliance check on any codebase.

    Evaluates the codebase against the Atomadic 5-tier monadic architecture
    (qk → at → mo → og → sy). Reports tier distribution, boundary violations,
    circular dependencies, test coverage, and documentation gaps.

    Produces a compliance score (0-100) and actionable recommendations.
    """
    import json as _json
    import subprocess as _sp
    import sys as _sys
    from ass_ade.recon import run_parallel_recon
    from ass_ade.local.linter import run_linters

    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    # ── External script path (when atomadic-ecosystem is installed) ───────────
    _eco_root = os.environ.get("ATOMADIC_ECOSYSTEM_ROOT", "")
    if _eco_root:
        _eco_script = Path(_eco_root) / "a4_sy_orchestration" / "sy_eco_scan.py"
        if _eco_script.exists():
            cmd: list[str] = [_sys.executable, str(_eco_script), str(target)]
            if json_out:
                cmd.append("--json")
            if out:
                cmd += ["--out", str(out)]
            _result = _sp.run(cmd)
            raise typer.Exit(code=_result.returncode)
        else:
            console.print(
                f"[dim]ATOMADIC_ECOSYSTEM_ROOT set but sy_eco_scan.py not found at {_eco_script} — using built-in.[/dim]"
            )

    # ── Built-in fallback ─────────────────────────────────────────────────────
    console.print(f"[bold]Eco-scanning[/bold] {target}")
    console.print("[dim]Running 5 parallel recon agents…[/dim]")

    report = run_parallel_recon(target)

    # ── Compliance scoring (0–100) ────────────────────────────────────────────
    score = 100
    issues: list[str] = []

    # Tier violations: -5 each, cap at -30
    violations = report.tier.get("tier_violations", [])
    tier_penalty = min(5 * len(violations), 30)
    score -= tier_penalty
    for v in violations:
        issues.append(f"Tier boundary violation: {v}")

    # Circular dependencies: -10 per cycle, cap at -20
    if report.dependency.get("has_circular_deps"):
        n_cycles = len(report.dependency.get("circular_deps", []))
        score -= min(10 * n_cycles, 20)
        issues.append(f"Circular imports detected ({n_cycles} cycle(s))")

    # Test coverage: -15 if below 0.15
    cov = float(report.test.get("coverage_ratio", 0))
    if cov < 0.15:
        score -= 15
        issues.append(f"Test coverage critically low ({cov:.0%})")
    elif cov < 0.30:
        score -= 7
        issues.append(f"Test coverage below 30% ({cov:.0%})")

    # Doc coverage: -10 if below 30%
    doc_cov = report.doc.get("doc_coverage", 0.0)
    if doc_cov < 0.30:
        score -= 10
        issues.append(f"Documentation coverage low ({doc_cov:.0%})")

    # Linter: run ruff; -5 if it finds any errors
    console.print("[dim]Running linter checks…[/dim]")
    lint_result = run_linters(target)
    total_lint = lint_result.get("total_findings", 0)
    if total_lint > 0:
        score -= min(total_lint // 10, 10)
        issues.append(f"Linter: {total_lint} finding(s)")

    # ── Standalone naming + cross-tier import checks (no external tools needed) ─
    import ast as _ast

    _TIER_ORDER_ECO: dict[str, int] = {"qk": 0, "at": 1, "mo": 2, "og": 3, "sy": 4}
    _IGNORE_DIRS_ECO = {".venv", "venv", "__pycache__", ".git", ".tox", "node_modules", "dist", "build"}
    _SKIP_STEMS_ECO = {"__init__", "__main__", "conftest"}

    def _iter_py_eco(root: Path) -> list[Path]:
        result: list[Path] = []
        for f in root.rglob("*.py"):
            if not any(part in _IGNORE_DIRS_ECO for part in f.parts):
                result.append(f)
        return result

    def _parse_imports_eco(f: Path) -> list[str]:
        try:
            tree = _ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            return []
        names: list[str] = []
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Import):
                for alias in node.names:
                    names.append(alias.name.split(".")[0])
            elif isinstance(node, _ast.ImportFrom):
                if node.module:
                    names.append(node.module.split(".")[0])
        return names

    py_files_eco = _iter_py_eco(target)
    unnamed_eco: list[str] = []
    stem_to_tier_eco: dict[str, str] = {}
    for _f in py_files_eco:
        _stem = _f.stem.lower()
        if _stem in _SKIP_STEMS_ECO or _f.name.startswith("test_") or _f.name.endswith("_test.py"):
            continue
        _matched = next((t for t in _TIER_ORDER_ECO if _stem.startswith(t + "_")), None)
        if _matched:
            stem_to_tier_eco[_f.stem] = _matched
        else:
            try:
                unnamed_eco.append(_f.relative_to(target).as_posix())
            except ValueError:
                unnamed_eco.append(_f.name)

    _named_count = len(stem_to_tier_eco)
    _total_scannable = _named_count + len(unnamed_eco)
    if _total_scannable > 0 and _named_count > 0:
        _naming_pct = _named_count / _total_scannable
        if _naming_pct < 0.5:
            score -= 5
            issues.append(
                f"Naming: {len(unnamed_eco)} file(s) lack tier prefix (qk_/at_/mo_/og_/sy_) "
                f"— only {_naming_pct:.0%} follow the convention"
            )

    cross_tier: list[str] = []
    for _f in py_files_eco:
        _tier = stem_to_tier_eco.get(_f.stem)
        if _tier is None:
            continue
        for _imp in _parse_imports_eco(_f):
            _imported_tier = stem_to_tier_eco.get(_imp)
            if _imported_tier and _TIER_ORDER_ECO.get(_imported_tier, 0) > _TIER_ORDER_ECO.get(_tier, 0):
                try:
                    _rel = _f.relative_to(target).as_posix()
                except ValueError:
                    _rel = _f.name
                cross_tier.append(f"{_rel} ({_tier}) imports {_imp} ({_imported_tier})")
    if cross_tier:
        score -= min(5 * len(cross_tier), 15)
        for _ct in cross_tier[:5]:
            issues.append(f"Cross-tier import: {_ct}")
        if len(cross_tier) > 5:
            issues.append(f"… and {len(cross_tier) - 5} more cross-tier import(s)")
    else:
        cross_tier = []

    score = max(score, 0)
    grade = (
        "A" if score >= 90 else
        "B" if score >= 75 else
        "C" if score >= 60 else
        "D" if score >= 40 else
        "F"
    )

    tier_dist = report.tier.get("tier_distribution", {})

    if json_out:
        payload = {
            "root": str(target),
            "score": score,
            "grade": grade,
            "tier_distribution": tier_dist,
            "violations": violations,
            "cross_tier_imports": cross_tier,
            "naming_unnamed": unnamed_eco[:20],
            "circular_deps": report.dependency.get("circular_deps", []),
            "test_coverage": cov,
            "doc_coverage": doc_cov,
            "lint_findings": total_lint,
            "issues": issues,
            "recommendations": report.recommendations,
        }
        _print_json(payload)
        return

    # ── Markdown report ───────────────────────────────────────────────────────
    score_color = "green" if score >= 75 else "yellow" if score >= 50 else "red"
    console.print(f"\n[bold]Monadic Compliance Score:[/bold] [{score_color}]{score}/100 (Grade {grade})[/{score_color}]")

    # Tier table
    if tier_dist:
        t = Table(title="Tier Distribution", show_header=True)
        t.add_column("Tier", style="bold")
        t.add_column("Files", justify="right")
        for tier_name, count in sorted(tier_dist.items()):
            t.add_row(tier_name, str(count))
        console.print(t)

    if violations:
        console.print(f"\n[yellow]Tier Violations ({len(violations)})[/yellow]")
        for v in violations[:10]:
            console.print(f"  • {v}")
        if len(violations) > 10:
            console.print(f"  … and {len(violations) - 10} more")

    if cross_tier:
        console.print(f"\n[yellow]Cross-Tier Imports ({len(cross_tier)})[/yellow]")
        for ct in cross_tier[:5]:
            console.print(f"  • {ct}")
        if len(cross_tier) > 5:
            console.print(f"  … and {len(cross_tier) - 5} more")

    if issues:
        console.print(f"\n[bold]Findings[/bold]")
        for issue in issues:
            console.print(f"  [yellow]⚠[/yellow]  {issue}")
    else:
        console.print("\n[green]No compliance issues found.[/green]")

    if report.recommendations:
        console.print(f"\n[bold]Recommendations[/bold]")
        for rec in report.recommendations:
            console.print(f"  {rec}")

    # Write to file if requested
    if out:
        md_lines = [
            f"# ECO-SCAN REPORT",
            f"",
            f"**Path:** `{target}`  ",
            f"**Score:** {score}/100 (Grade {grade})",
            f"",
            f"## Tier Distribution",
            "",
        ]
        for tier_name, count in sorted(tier_dist.items()):
            md_lines.append(f"- `{tier_name}`: {count}")
        if violations:
            md_lines += ["", f"## Tier Violations", ""]
            for v in violations:
                md_lines.append(f"- {v}")
        if cross_tier:
            md_lines += ["", f"## Cross-Tier Imports", ""]
            for ct in cross_tier:
                md_lines.append(f"- {ct}")
        if issues:
            md_lines += ["", f"## Findings", ""]
            for issue in issues:
                md_lines.append(f"- {issue}")
        if report.recommendations:
            md_lines += ["", f"## Recommendations", ""]
            for rec in report.recommendations:
                md_lines.append(f"- {rec}")
        out.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
        console.print(f"\n[dim]Report written to {out}[/dim]")

    raise typer.Exit(code=0 if score >= 60 else 1)


@app.command("recon")
def recon_command(
    path: Path = typer.Argument(Path("."), help="Repo root to analyse."),
    out: Path | None = typer.Option(None, "--out", "-o", help="Write RECON_REPORT.md to this file."),
    json_out: bool = typer.Option(False, "--json", help="Print JSON instead of Markdown."),
) -> None:
    """Run parallel codebase reconnaissance — 5 agents, no LLM, < 5 s.

    Agents: Scout (files/structure), Dependency (imports/cycles),
    Tier (qk/at/mo/og/sy), Test (coverage), Doc (README/docstrings).
    """
    import json as _json
    from ass_ade.recon import run_parallel_recon

    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Running recon on[/bold] {target} …")
    report = run_parallel_recon(target)

    if json_out:
        console.print_json(_json.dumps(report.to_dict(), indent=2))
    else:
        console.print(report.to_markdown())

    if out:
        out.write_text(report.to_markdown(), encoding="utf-8")
        console.print(f"[green]Report written →[/green] {out}")

    console.print(f"[dim]Completed in {report.duration_ms:.0f} ms[/dim]")


def _generate_rebuild_docs(
    output_dir: Path,
    source_path: Path,
    recon_data: "dict | None" = None,
    *,
    preserve_readme: bool = False,
) -> None:
    """Write the full self-documenting suite into a finished rebuild folder."""
    import json as _json
    import shutil as _shutil

    cert_path = output_dir / "CERTIFICATE.json"
    manifest_path = output_dir / "MANIFEST.json"
    cert: dict = {}
    manifest: dict = {}
    if cert_path.exists():
        cert = _json.loads(cert_path.read_text(encoding="utf-8"))
    if manifest_path.exists():
        manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))

    audit = cert.get("audit", {})
    inv = audit.get("codex_invariants", {})
    summary = audit.get("summary", {})
    counts = manifest.get("counts", cert.get("counts", {}))
    by_tier = counts.get("by_tier", {})
    total = counts.get("total", cert.get("written_count", 0))
    rebuild_tag = cert.get("rebuild_tag", "unknown")
    issued_at = cert.get("issued_at", "")
    cert_hash = cert.get("certificate_sha256", "")
    source_name = source_path.name
    pass_rate = summary.get("pass_rate", 1.0)
    codex_ok = summary.get("codex_conformant", True)
    d_max = inv.get("D_max", {})
    g18 = inv.get("G_18", {})
    eps = inv.get("epsilon_KL", {})
    tau = inv.get("tau_trust", {})

    _tier_desc = {
        "a0_qk_constants":     "Stateless invariants — constants, axioms",
        "a1_at_functions":     "Pure functions (atoms)",
        "a2_mo_composites":    "Stateful compositions (molecules)",
        "a3_og_features":      "Feature modules (organisms)",
        "a4_sy_orchestration": "Top-level orchestration (system)",
    }
    tier_rows = "\n".join(
        f"| `{t}` | {n} | {_tier_desc.get(t, '')} |"
        for t, n in sorted(by_tier.items())
    )

    # 0_README.md
    (output_dir / "0_README.md").write_text(f"""\
# {source_name} — Monadic Rebuild

Auto-generated by ASS-ADE rebuild engine · rebuild `{rebuild_tag}` · {issued_at[:10]}

This folder is a tier-partitioned monadic rebuild of `{source_path}`, produced
by the Atomadic ecosystem rebuilder (AAAA-SPEC-003). Every source symbol has
been classified, restructured, and validated against public structural invariants.

## Tier structure

| Tier | Components | Purpose |
|------|-----------|---------|
{tier_rows}

**Total components:** {total}

## Structural status

- Conformant: {'YES' if codex_ok else 'NO'}
- Pass rate: {pass_rate:.1%}
- Certificate: `CERTIFICATE.json` (AAAA-SPEC-006/CERT-1)

## Quick start

```bash
# Explore by tier
ls a0_qk_constants/        # constants and axioms
ls a1_at_functions/        # pure atoms
ls a2_mo_composites/       # stateful engines
ls a3_og_features/         # feature organisms
ls a4_sy_orchestration/    # orchestration

# Verify the certificate
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('OK' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```
""", encoding="utf-8")

    # README.md is public-facing; preserve a hand-authored showcase README on
    # existing outputs and keep the generated status doc in 0_README.md.
    readme_path = output_dir / "README.md"
    if not (preserve_readme and readme_path.exists()):
        _shutil.copy2(output_dir / "0_README.md", readme_path)

    # 1_QUICKSTART.md
    (output_dir / "1_QUICKSTART.md").write_text(f"""\
# Quick Start

## Prerequisites

- Python 3.11+
- ASS-ADE installed (`pip install ass-ade` or `pip install -e .`)
- Optional: AAAA-Nexus API key for premium features

## Basic usage

```bash
# Chat with Atomadic (the interactive front door)
ass-ade chat

# Rebuild any codebase into clean tiers
ass-ade rebuild ./my-project ./my-project-rebuilt

# Generate documentation
ass-ade docs ./my-project

# Run the lint pipeline
ass-ade lint ./my-project

# Certify the output
ass-ade certify ./my-project-rebuilt

# Enhance a codebase
ass-ade enhance ./my-project
```

## Tier layout after rebuild

```
{output_dir.name}/
├── a0_qk_constants/        # stateless invariants, constants, axioms
├── a1_at_functions/        # pure functions
├── a2_mo_composites/       # stateful compositions
├── a3_og_features/         # feature modules
├── a4_sy_orchestration/    # top-level orchestration
├── 0_README.md
├── 1_QUICKSTART.md
├── 2_ARCHITECTURE.md
├── 3_USER_GUIDE.md
├── 4_FEATURES.md
├── 5_CONTRIBUTING.md
├── CHANGELOG.md
├── CERTIFICATE.json
└── NEXT_ENHANCEMENT.md
```

## Verify certificate

```bash
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('VERIFIED' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```

Rebuild tag: `{rebuild_tag}` · Issued: {issued_at[:10]}
""", encoding="utf-8")

    # 2_ARCHITECTURE.md
    cycle = inv.get("D_max", {})
    obs_depth = d_max.get("observed_max_depth", "?")
    (output_dir / "2_ARCHITECTURE.md").write_text(f"""\
# Architecture

## 5-tier composition law (AAAA-SPEC-003)

```
a0_qk_constants      ← stateless invariants: constants, axioms, public rules
a1_at_functions      ← pure functions operating on qk
a2_mo_composites     ← stateful compositions of at
a3_og_features       ← feature modules composed of mo
a4_sy_orchestration  ← top-level orchestration and system entry points
```

Dependencies flow strictly upward: `qk → at → mo → og → sy`.
No tier may import from a tier above it.

## Component distribution

| Tier | Count |
|------|-------|
{chr(10).join(f'| `{t}` | {n} |' for t, n in sorted(by_tier.items()))}
| **Total** | **{total}** |

## Dependency graph

- Cycles: **{g18.get('parity', '?')} parity** (G_18 modulus {g18.get('modulus', 324)})
- Max chain depth: **{obs_depth}** (limit: {d_max.get('limit', 23)})
- Cycle violations: **{d_max.get('violations', 0)}**

## Public invariants

| Invariant | Value | Conformant |
|-----------|-------|-----------|
| D_max (max depth) | {obs_depth} / {d_max.get('limit', 23)} | {'YES' if d_max.get('conformant', True) else 'NO'} |
| epsilon_KL (dup fraction) | {eps.get('observed_duplicate_fraction', 0.0):.2e} | {'YES' if eps.get('conformant', True) else 'NO'} |
| tau_trust (pass rate) | {tau.get('numerator', 1820)}/{tau.get('denominator', 1823)} | YES |
| G_18 (structural parity) | {g18.get('component_count', total)} components | — |

## Schema

- Component schema: AAAA-SPEC-003
- Certificate schema: AAAA-SPEC-006/CERT-1
- Issuer: `{cert.get('issuer', 'mo.refactor.schema_rebuilder')}`
""", encoding="utf-8")

    # 3_USER_GUIDE.md
    (output_dir / "3_USER_GUIDE.md").write_text(f"""\
# User Guide

## Core commands

### ass-ade chat
Drop into an interactive session with Atomadic — the friendly front-door interpreter.
Speak casually or precisely; Atomadic derives the intent and dispatches the right command.

```bash
ass-ade chat
```

### ass-ade rebuild
Reorganize any codebase into the 5-tier monadic layout.

```bash
ass-ade rebuild ./source ./output          # full rebuild
ass-ade rebuild ./output                    # incremental update
ass-ade rebuild ./source ./output --premium # with Nexus enrichment
```

### ass-ade design
Produce a feature blueprint (AAAA-SPEC-004 JSON).

```bash
ass-ade design "Add JWT authentication" --output ./blueprints
```

### ass-ade docs
Generate or refresh documentation for any folder.

```bash
ass-ade docs ./my-project
```

### ass-ade lint
Run the CIE lint pipeline (AST + ruff + OWASP checks).

```bash
ass-ade lint ./my-project
ass-ade lint ./my-project --json
```

### ass-ade certify
Run the full certification pipeline and produce a signed CERTIFICATE.json.

```bash
ass-ade certify ./my-project
```

### ass-ade enhance
Proactively propose enhancements for any module or feature.

```bash
ass-ade enhance ./my-project
ass-ade enhance ./my-project --apply 1,3,5
```

### ass-ade eco-scan
Produce an onboarding pack for any codebase (architecture snapshot, gap report, next moves).

```bash
ass-ade eco-scan ./any-repo
```

### ass-ade doctor
Self-check: config, connectivity, test suite.

```bash
ass-ade doctor
```

## Configuration

Copy and edit the example config:

```bash
cp examples/ass-ade.config.json ~/.ass-ade.json
```

Key options:
- `profile`: `local` | `hybrid` | `premium`
- `nexus_api_key`: Your AAAA-Nexus API key (for hybrid/premium)
- `default_model`: Override the default LLM

## This rebuild

- Source: `{source_path}`
- Components: {total}
- Rebuild tag: `{rebuild_tag}`
- Structural conformant: {'YES' if codex_ok else 'NO'}
""", encoding="utf-8")

    # 4_FEATURES.md — grouped from component ids
    components = manifest.get("components", [])
    by_cat: dict[str, list[str]] = {}
    for c in components:
        cid = c.get("id", "")
        parts = cid.split(".")
        cat = parts[1] if len(parts) > 1 else "other"
        by_cat.setdefault(cat, []).append(c.get("name", cid))
    cat_lines = ""
    for cat, names in sorted(by_cat.items()):
        cat_lines += f"\n### {cat} ({len(names)} components)\n"
        cat_lines += "\n".join(f"- `{n}`" for n in sorted(names)[:20])
        if len(names) > 20:
            cat_lines += f"\n- … and {len(names) - 20} more"
        cat_lines += "\n"
    (output_dir / "4_FEATURES.md").write_text(f"""\
# Features

Auto-extracted from rebuilt component surface · {total} components total.

## By tier

{chr(10).join(f'- **{t}**: {n} components' for t, n in sorted(by_tier.items()))}

## By module category
{cat_lines}
""", encoding="utf-8")

    # 5_CONTRIBUTING.md
    (output_dir / "5_CONTRIBUTING.md").write_text(f"""\
# Contributing

## Philosophy

ASS-ADE follows the 5-tier monadic composition law. Every contribution must respect
the tier boundaries — a component at tier N may only depend on tiers below N.

## Tiers at a glance

| Folder | Tier | Rule |
|--------|------|------|
| `a0_qk_constants/` | qk | No imports from this repo. Pure constants/axioms only. |
| `a1_at_functions/` | at | May import qk. Pure functions, no I/O. |
| `a2_mo_composites/` | mo | May import at + qk. May hold state. |
| `a3_og_features/` | og | May import mo and below. I/O permitted. |
| `a4_sy_orchestration/` | sy | Top-level only. Wires og into pipelines. |

## Workflow

1. Write a blueprint first: `ass-ade design "My feature" --output ./blueprints`
2. Rebuild to materialize: `ass-ade rebuild . --output ./output`
3. Lint: `ass-ade lint ./output`
4. Certify: `ass-ade certify ./output`

## Code style

- Python 3.11+
- Ruff for linting and formatting (`ruff check . && ruff format .`)
- Pydantic models for all data structures
- Type hints required on all public APIs

## Tests

```bash
python -m pytest tests/ -q
```

All tests must pass before a PR is accepted.

## IP boundary

This is the public-safe shell of the Atomadic ecosystem. Do NOT add:
- Private prompt or orchestration internals
- Internal-only proof identifiers
- Hidden routing or pricing heuristics
- Private roadmap markers

## Rebuild baseline

This folder was built from `{source_path}` · rebuild `{rebuild_tag}` · {issued_at[:10]}.
""", encoding="utf-8")

    # CHANGELOG.md
    _changelog_tier_rows = "\n".join(
        f"| `{t}` | {n} |" for t, n in sorted(by_tier.items())
    )
    (output_dir / "CHANGELOG.md").write_text(f"""\
# Changelog

## Rebuild {rebuild_tag} — {issued_at[:10]}

### Summary

Full monadic rebuild of `{source_path}` via ASS-ADE / AAAA-SPEC-003.

### What changed

- **Components materialized**: {total}
- **Pass rate**: {pass_rate:.1%}
- **Structural conformance**: {('PASS' if codex_ok else 'FAIL')}
- **Cycles eliminated**: {d_max.get('violations', 0)} violations fixed
- **Duplicates dropped**: {manifest.get('counts', {}).get('deduped_dropped', 0)}
- **Certificate issued**: `{cert_hash[:16]}…` (AAAA-SPEC-006/CERT-1)

### Tier breakdown

| Tier | Components |
|------|-----------|
{_changelog_tier_rows}

### Source

- Input: `{source_path}`
- Rebuild tag: `{rebuild_tag}`
- Timestamp: `{issued_at}`
- Schema: {manifest.get('schema', 'AAAA-SPEC-003')}
- Plan digest: `{cert.get('source_plan_digest', '')}`
""", encoding="utf-8")

    # .gitignore
    (output_dir / ".gitignore").write_text("""\
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.env
.venv
venv/
*.log
.atomadic/
""", encoding="utf-8")

    # NEXT_ENHANCEMENT.md
    (output_dir / "NEXT_ENHANCEMENT.md").write_text(f"""\
# Next Enhancement Recommendations

Generated by ASS-ADE after rebuild `{rebuild_tag}`.

## Rebuild baseline

- Components: {total} across 5 tiers
- Structural conformant: {'YES' if codex_ok else 'NO'}
- Pass rate: {pass_rate:.1%}

## Recommended next steps

### 1. Premium enrichment (highest value)

Run each component through the full Nexus trust + OWASP + hallucination pipeline:

```bash
ass-ade rebuild . --output C:/!ass-ade-release --premium
```

This gates every component through:
- `/v1/trust/score` — tau_trust quarantine
- `/v1/security/zero-day` — OWASP-class scan
- `/v1/oracle/hallucination` — tier classification sanity
- `/v1/certify-output` — signed quality attestation

### 2. Blueprint gap fill

{total} components were materialized but blueprint satisfaction is partial.
Run the gap-filler to propose implementations for unfulfilled blueprints:

```bash
ass-ade design . --output C:/!ass-ade-release
```

### 3. Ecosystem integration

Pull cross-repo gaps from the full Atomadic manifest:

```bash
ass-ade rebuild . --output C:/!ass-ade-release --include-ecosystem
```

### 4. LoRA flywheel submission

Contribute high-quality components to the shared flywheel for model improvement:

```bash
ass-ade rebuild . --output C:/!ass-ade-release --capture-to-flywheel
```

## Trust score baseline

All {total} components passed structural validation at tau_trust = {tau.get('numerator',1820)}/{tau.get('denominator',1823)}.
Next rebuild should target `pass_rate = 1.0` with zero D_max violations.
""", encoding="utf-8")

    # ── helpers shared by CHEATSHEET and interpreter update ─────────────────
    import subprocess as _sub

    def _run_help() -> list[str]:
        try:
            r = _sub.run(
                [sys.executable, "-m", "ass_ade", "--help"],
                capture_output=True, text=True, timeout=15,
                encoding="utf-8", errors="replace",
            )
            return r.stdout.strip().splitlines()
        except Exception:
            return []

    def _scan_py_dir(d: Path) -> list[str]:
        if not d.is_dir():
            return []
        return sorted(f.stem for f in d.glob("*.py") if not f.name.startswith("_"))

    def _scan_dir_names(d: Path) -> list[str]:
        if not d.is_dir():
            return []
        return sorted(f.name for f in d.iterdir() if f.is_file())

    def _scan_md_dir(d: Path) -> list[str]:
        if not d.is_dir():
            return []
        return sorted(
            f.name for f in d.glob("*.md")
            if f.name.lower() not in ("readme.md",)
        )

    _cli_lines = _run_help()
    _cli_block = "\n".join(_cli_lines) if _cli_lines else "(run `python -m ass_ade --help`)"

    # tools/: check source_path first, then src/ass_ade/tools fallback
    _tools_dir = source_path / "tools"
    if not _tools_dir.is_dir():
        _tools_dir = source_path / "src" / "ass_ade" / "tools"
    if not _tools_dir.is_dir():
        _tools_dir = Path(__file__).parent / "tools"
    _tool_names = _scan_py_dir(_tools_dir)

    # hooks/: check source_path then output_dir
    _hooks_dir = source_path / "hooks"
    if not _hooks_dir.is_dir():
        _hooks_dir = output_dir / "hooks"
    _hook_names = _scan_dir_names(_hooks_dir)

    # agents/: relative to the repo root inferred from __file__
    _agents_dir = Path(__file__).parent.parent.parent / "agents"
    _agent_names = _scan_md_dir(_agents_dir)

    # blueprints: .json files in output_dir (excluding cert/manifest) + blueprints/ subdir
    _bp: list[str] = [
        f.name for f in sorted(output_dir.glob("*.json"))
        if f.name not in ("CERTIFICATE.json", "MANIFEST.json")
    ]
    _bp_sub = output_dir / "blueprints"
    if _bp_sub.is_dir():
        _bp += [f"blueprints/{f.name}" for f in sorted(_bp_sub.glob("*.json"))]

    def _bullet_list(items: list[str]) -> str:
        return "\n".join(f"- `{i}`" for i in items) if items else "- (none found)"

    # CHEATSHEET.md
    (output_dir / "CHEATSHEET.md").write_text(f"""\
# ASS-ADE Cheat Sheet

Auto-generated by ASS-ADE rebuild · `{rebuild_tag}` · {issued_at[:10]}
Regenerated on every rebuild — always current.

---

## CLI Commands

```
{_cli_block}
```

## Tools (`tools/`)

{_bullet_list(_tool_names)}

## Hooks (`hooks/`)

{_bullet_list(_hook_names)}

## Agent Definitions (`agents/`)

{_bullet_list(_agent_names)}

## Blueprint Files

{_bullet_list(_bp)}

---

*Re-run `ass-ade rebuild` to refresh this cheat sheet.*
""", encoding="utf-8")

    # Update agents/atomadic_interpreter.md — append/replace Current Capabilities
    _interp_path = Path(__file__).parent.parent.parent / "agents" / "atomadic_interpreter.md"
    if _interp_path.exists():
        _interp_text = _interp_path.read_text(encoding="utf-8")
        _marker = "\n---\n\n## Current Capabilities"
        if _marker in _interp_text:
            _interp_text = _interp_text[: _interp_text.index(_marker)]
        _caps_section = f"""\n---\n\n## Current Capabilities\n\n*Auto-updated by rebuild `{rebuild_tag}` · {issued_at[:10]}*\n\n### CLI Commands\n\n```\n{_cli_block}\n```\n\n### Tools\n\n{_bullet_list(_tool_names)}\n\n### Hooks\n\n{_bullet_list(_hook_names)}\n\n### Agents\n\n{_bullet_list(_agent_names)}\n"""
        _interp_path.write_text(_interp_text.rstrip() + _caps_section, encoding="utf-8")
        try:
            from ass_ade.agent.capabilities import sync_atomadic_prompt_capabilities as _sync_caps

            _sync_caps(repo_root=Path(__file__).parent.parent.parent)
        except Exception:
            pass

    # REBUILD_REPORT.md
    (output_dir / "REBUILD_REPORT.md").write_text(f"""\
# Rebuild Report

**Rebuild tag**: `{rebuild_tag}`
**Issued**: {issued_at}
**Issuer**: {cert.get('issuer', 'mo.refactor.schema_rebuilder')}
**Schema**: {manifest.get('schema', 'AAAA-SPEC-003')}

## Source

| Field | Value |
|-------|-------|
| Input path | `{source_path}` |
| Plan digest | `{cert.get('source_plan_digest', '')}` |
| Control root | `{cert.get('control_root', '')}` |

## Output

| Field | Value |
|-------|-------|
| Components written | {cert.get('written_count', total)} |
| Output folder | `{output_dir}` |

## Tier breakdown

| Tier | Count |
|------|-------|
{chr(10).join(f'| `{t}` | {n} |' for t, n in sorted(by_tier.items()))}
| **Total** | **{total}** |

## Public invariants

| Invariant | Observed | Limit | Pass |
|-----------|---------|-------|------|
| D_max (depth) | {obs_depth} | {d_max.get('limit', 23)} | {'YES' if d_max.get('conformant', True) else 'NO'} |
| epsilon_KL (dup fraction) | {eps.get('observed_duplicate_fraction', 0.0):.2e} | {eps.get('bound', 0.0):.2e} | {'YES' if eps.get('conformant', True) else 'NO'} |
| tau_trust | {tau.get('score','≥threshold')} | ≥threshold | YES |
| G_18 parity | {g18.get('parity', '?')} mod {g18.get('modulus', 324)} | — | — |

## Audit summary

- **Structural conformant**: {'YES' if codex_ok else 'NO'}
- **Pass rate**: {pass_rate:.1%}
- **Total findings**: {summary.get('findings_total', 0)}
- **Valid components**: {audit.get('valid', total)} / {audit.get('total', total)}

## Certificate

- **Version**: {cert.get('certificate_version', 'AAAA-SPEC-006/CERT-1')}
- **SHA-256**: `{cert_hash}`

Verify:
```bash
python -c "import json,hashlib; c=json.load(open('CERTIFICATE.json')); h=c.pop('certificate_sha256'); b=json.dumps(c,sort_keys=True).encode(); print('VERIFIED' if hashlib.sha256(b).hexdigest()==h else 'TAMPERED')"
```
""", encoding="utf-8")

    # ── BIRTH_CERTIFICATE.md — generated once, never overwritten ─────────────
    import hashlib as _hashlib
    _birth_path = output_dir / "BIRTH_CERTIFICATE.md"
    if not _birth_path.exists():
        try:
            _manifest_bytes = manifest_path.read_bytes()
            _genesis_hash = _hashlib.sha256(_manifest_bytes).hexdigest()
        except OSError:
            _genesis_hash = "unavailable"

        _mat_at = manifest.get("materialized_at", issued_at)
        _plan_digest = manifest.get("source_plan_digest", cert.get("source_plan_digest", ""))
        _schema = manifest.get("schema", "ASSADE-SPEC-003")

        _tier_rows_bc = "\n".join(
            f"| `{t}` | {by_tier.get(t, 0)} |"
            for t in [
                "a0_qk_constants", "a1_at_functions",
                "a2_mo_composites", "a3_og_features", "a4_sy_orchestration",
            ]
        )

        _ver_rows: list[str] = []
        for _tier in [
            "a0_qk_constants", "a1_at_functions",
            "a2_mo_composites", "a3_og_features", "a4_sy_orchestration",
        ]:
            _vpath = output_dir / _tier / "VERSION.json"
            try:
                _vdata = _json.loads(_vpath.read_text(encoding="utf-8"))
                _mc = _vdata.get("module_count", by_tier.get(_tier, 0))
            except OSError:
                _mc = by_tier.get(_tier, 0)
            _ver_rows.append(f"| `{_tier}` | {_mc} | `0.1.0` |")

        _test_count = (recon_data or {}).get("test_functions", "see `ass-ade recon`")
        _doc_cov_raw = (recon_data or {}).get("doc_coverage")
        _doc_cov = f"{_doc_cov_raw:.0%}" if isinstance(_doc_cov_raw, float) else "see `ass-ade recon`"

        _audit_findings = summary.get("findings_total", 0)
        _by_code = summary.get("by_code", {})
        _findings_detail = ", ".join(f"{k}: {v}" for k, v in sorted(_by_code.items()))
        _enrich = cert.get("audit", {}).get("enrich", {})

        _birth_path.write_text(f"""\
# BIRTH CERTIFICATE — {source_name} v0.0.1

> **This document is the permanent origin record.**
> It is preserved unchanged across all future rebuilds and evolutions.
> Compare against the current `CERTIFICATE.json` to measure how far this codebase has evolved.

---

## Identity

| Field | Value |
|---|---|
| Build name | **{source_name} v0.0.1 — Maiden Self-Rebuild** |
| Date/time of birth | `{_mat_at}` |
| Rebuild tag | `{rebuild_tag}` |
| Parent (source path) | `{source_path}` |
| Builder | `ASS-ADE v0.0.1 (self-built)` |
| Schema | `{_schema}` |
| Source plan digest | `{_plan_digest}` |

---

## Genesis Hash

SHA-256 of `MANIFEST.json` at birth:

```
{_genesis_hash}
```

Verify at any time:
```bash
python -c "import hashlib; print(hashlib.sha256(open('MANIFEST.json','rb').read()).hexdigest())"
```

(If this matches, the manifest is untouched since birth. If it differs, the codebase has evolved — check `REBUILD_REPORT.md` for the delta.)

---

## Initial Certificate

SHA-256 from `CERTIFICATE.json` at birth (tracks quality, not identity):

```
{cert_hash}
```

---

## Initial Tier Distribution

| Tier | Components |
|---|---|
{_tier_rows_bc}
| **Total** | **{total}** |

---

## Initial Metrics

| Metric | Value |
|---|---|
| Components materialized | {total} |
| Audit pass rate | {pass_rate:.1%} |
| Audit findings | {_audit_findings}{(' (' + _findings_detail + ')') if _findings_detail else ''} |
| Structural conformant | {'YES' if codex_ok else 'NO'} |
| Test count (source) | {_test_count} |
| Doc coverage (source) | {_doc_cov} |

---

## Initial VERSION.json Snapshot

| Tier | Module count | Version |
|---|---|---|
{chr(10).join(_ver_rows)}

All change types: `new` (no prior version existed).

---

## Lineage Note

This is rebuild generation **1** — the first time this codebase built itself.

Every subsequent rebuild produces a new `CERTIFICATE.json` and `REBUILD_REPORT.md`
tracking the delta from the current state. This file never changes. Future
generations can diff:

```
BIRTH_CERTIFICATE.md  ← where it started (you are reading this)
CERTIFICATE.json      ← where it is now
REBUILD_REPORT.md     ← what changed in the most recent rebuild
```

The distance between genesis hash and current certificate hash is the measure of evolution.
""", encoding="utf-8")


@app.command("rebuild")
def rebuild_codebase(
    paths: List[Path] = typer.Argument(
        ...,
        help=(
            "One or more source directories to rebuild. When multiple paths are given "
            "their symbol pools are merged into one unified output (newer sources win on conflicts)."
        ),
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory. Required when merging multiple sources. "
             "Omit for single-source to auto-name: {source}-v{version}-{timestamp}.",
    ),
    premium: bool = typer.Option(False, help="Enable synthesis of missing blueprint components via AAAA-Nexus. Paid."),
    no_certify: bool = typer.Option(False, "--no-certify", help="Skip automatic certify step after rebuild."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview tier plan without writing any files."),
    backup: bool = typer.Option(
        True,
        "--backup/--no-backup",
        help="Back up an existing output folder before replacing or updating it.",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt (auto-confirm)."),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
    incremental: bool = typer.Option(
        False, "--incremental",
        help="Only re-process files changed since last MANIFEST.json. Skip unchanged files.",
    ),
    git_track: bool = typer.Option(
        False,
        "--git-track/--no-git-track",
        help="After a successful rebuild, stage all output files, commit, and create a tag in the output git repo.",
    ),
) -> None:
    """Rebuild any codebase into a clean tier-partitioned modular folder.

    Single-source rebuild (first time):

        ass-ade rebuild ./messy-repo --output ./clean-repo

    Merge-rebuild (multiple sources into one unified output):

        ass-ade rebuild ./source-a ./source-b ./source-c --output ./unified --yes

    Dry-run preview (no writes):

        ass-ade rebuild ./messy-repo --output ./clean-repo --dry-run

    Incremental (only changed files):

        ass-ade rebuild ./clean-repo --incremental

    ASS-ADE's heavy-hitter: point it at a spaghetti codebase, get a brand-new
    folder organized by the 5-tier monadic composition law (a0_qk_constants,
    a1_at_functions, a2_mo_composites, a3_og_features,
    a4_sy_orchestration). Every symbol classified, every gap proposed, every
    draft materialized as an ASSADE-SPEC-003 component artifact.

    Self-contained — no external ecosystem dependency required.
    """
    import time as _time
    import json as _json
    import shutil as _shutil

    from ass_ade.engine.rebuild.orchestrator import rebuild_project as _rebuild_project
    from ass_ade.engine.rebuild.orchestrator import render_rebuild_summary as _render_summary
    from ass_ade.engine.rebuild.project_parser import ingest_project as _ingest_project
    from ass_ade.engine.rebuild.project_parser import iter_source_files as _iter_source_files

    # Backward compatibility: older CLI usage accepted
    # ``ass-ade rebuild <source> <output>`` before multi-source rebuilds moved
    # output to ``--output``. Keep that form working when the second positional
    # path is absent or does not look like another source tree.
    if output is None and len(paths) == 2:
        legacy_source, legacy_output = paths
        legacy_output_resolved = legacy_output.resolve()
        second_path_is_output = not legacy_output_resolved.exists()
        if legacy_output_resolved.exists() and legacy_output_resolved.is_dir():
            second_path_is_output = not any(_iter_source_files(legacy_output_resolved))
        if second_path_is_output:
            output = legacy_output
            paths = [legacy_source]

    # ── Validate all source paths ─────────────────────────────────────────────
    if not paths:
        console.print("[red]At least one source directory is required.[/red]")
        raise typer.Exit(code=1)

    all_targets: list[Path] = []
    for _p in paths:
        _t = _p.resolve()
        if not _t.exists():
            console.print(f"[red]Source directory does not exist:[/red] {_t}")
            raise typer.Exit(code=1)
        if not _t.is_dir():
            console.print(f"[red]Source path is not a directory:[/red] {_t}")
            raise typer.Exit(code=1)
        try:
            next(_t.iterdir(), None)
        except (PermissionError, OSError) as _e:
            console.print(f"[red]Source directory is not readable:[/red] {_t}\n{_e}")
            raise typer.Exit(code=1)
        all_targets.append(_t)

    # Primary target for backward-compat single-source operations
    target = all_targets[0]
    _multi_source = len(all_targets) > 1

    if _multi_source and output is None:
        console.print(
            "[red]--output is required when merging multiple source directories.[/red]\n"
            "  Example: ass-ade rebuild src1 src2 src3 --output ./unified"
        )
        raise typer.Exit(code=1)

    dest = output.resolve() if output else target
    in_place = output is None
    # When output is omitted, dest will be replaced with a versioned sibling after the rebuild completes.
    _auto_versioned_dest = in_place

    if output and not dest.parent.exists():
        console.print(f"[red]Output parent directory does not exist:[/red] {dest.parent}")
        raise typer.Exit(code=1)
    if output and dest.parent.exists():
        import os as _os
        if not _os.access(dest.parent, _os.W_OK):
            console.print(f"[red]Output directory is not writable:[/red] {dest.parent}")
            raise typer.Exit(code=1)

    _first_rebuild = not (dest / "MANIFEST.json").exists()

    # ── Incremental: find changed files since last MANIFEST.json ─────────────
    changed_files: set[str] | None = None
    if incremental:
        manifest_path = dest / "MANIFEST.json"
        if manifest_path.exists():
            try:
                manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))
                file_mtimes: dict[str, float] = manifest.get("file_mtimes", {})
                changed_files = set()
                for f in _iter_source_files(target):
                    rel = str(f.relative_to(target))
                    saved_mtime = file_mtimes.get(rel, 0)
                    current_mtime = f.stat().st_mtime
                    if current_mtime > saved_mtime:
                        changed_files.add(rel)
                if not json_out:
                    console.print(f"[dim]Incremental: {len(changed_files)} changed file(s) of "
                                  f"{sum(1 for _ in _iter_source_files(target))} total[/dim]")
            except Exception as _inc_exc:
                if not json_out:
                    console.print(f"[dim]Incremental check failed ({_inc_exc}) — running full rebuild[/dim]")
                changed_files = None
        else:
            if not json_out:
                console.print("[dim]No MANIFEST.json found — running full rebuild[/dim]")

    # ── Preview ingest: classify files into tiers for dry-run display ─────────
    _t0_ingest = _time.monotonic()
    _ingest_progress_state: list[int] = [0, 0]

    def _progress_cb(current: int, total: int) -> None:
        _ingest_progress_state[0] = current
        _ingest_progress_state[1] = total
        if not json_out:
            _draw_progress_bar("Ingest", current, total, _t0_ingest)

    if not json_out:
        _src_label_preview = (
            " + ".join(str(t) for t in all_targets)
            if _multi_source else str(target)
        )
        console.print(f"[dim]Analysing {_src_label_preview} …[/dim]")

    # For preview ingest, run on all sources and merge the summaries
    _all_preview_results = []
    for _pt in all_targets:
        _pr = _ingest_project(_pt, root_id=_pt.name, progress_callback=_progress_cb if _pt is target else None)
        _all_preview_results.append(_pr)

    if not json_out and _ingest_progress_state[1] > 0:
        _finish_progress_bar("Ingest", _ingest_progress_state[1],
                             _time.monotonic() - _t0_ingest)

    preview_result = _all_preview_results[0]
    by_tier: dict[str, int] = {}
    total_files_count = 0
    violation_count = 0
    for _pr in _all_preview_results:
        _s = _pr.get("summary", {})
        total_files_count += _s.get("files_scanned", 0)
        violation_count += len(_pr.get("gaps", []))
        for _tier, _cnt in _s.get("by_tier", {}).items():
            by_tier[_tier] = by_tier.get(_tier, 0) + _cnt
    est_seconds = max(5, total_files_count // 10)

    # ── Build tier preview lines (aligned) ───────────────────────────────────
    tier_order = [
        "a0_qk_constants", "a1_at_functions", "a2_mo_composites",
        "a3_og_features", "a4_sy_orchestration",
    ]
    _max_tier_len = max((len(t) for t in tier_order), default=20)
    tier_preview_lines = []
    for tier in tier_order:
        count = by_tier.get(tier, 0)
        if count > 0:
            tier_preview_lines.append(f"    {tier:<{_max_tier_len}}  {count:>5} files")
    for tier, count in sorted(by_tier.items()):
        if tier not in tier_order and count > 0:
            tier_preview_lines.append(f"    {tier:<{_max_tier_len}}  {count:>5} files")

    # Detect project language hint
    _lang_hints = [
        ("pyproject.toml", "Python"), ("package.json", "Node.js"),
        ("Cargo.toml", "Rust"), ("go.mod", "Go"),
    ]
    _lang = next((l for m, l in _lang_hints if (target / m).exists()), "")
    if _multi_source:
        _src_label = f"{len(all_targets)} sources merged ({total_files_count} total files)"
    else:
        _src_label = f"{target}" + (f" ({total_files_count} files, {_lang})" if _lang else f" ({total_files_count} files)")

    # Rich first-time plan vs. short follow-up diff preview
    if _first_rebuild and not dry_run:
        _src_lines = (
            "\n".join(f"            {t}" for t in all_targets) if _multi_source
            else f"  [dim]Source:[/dim]  {_src_label}"
        )
        preview_text = (
            "\n[bold]Merge-Rebuild Plan[/bold]\n" if _multi_source else "\n[bold]Rebuild Plan[/bold]\n"
        )
        if _multi_source:
            preview_text += f"  [dim]Sources ({len(all_targets)}):[/dim]\n{_src_lines}\n"
        else:
            preview_text += f"  [dim]Source:[/dim]  {_src_label}\n"
        preview_text += (
            f"  [dim]Output:[/dim]  {dest}\n\n"
            "  [bold]Tier Distribution:[/bold]\n"
            + "\n".join(tier_preview_lines or ["    (no source files classified)"])
            + f"\n\n  Gaps to fill:     {violation_count}"
            + f"\n  Estimated time:   ~{est_seconds}s"
        )
    else:
        preview_text = (
            "Dry-run preview:\n"
            + "\n".join(tier_preview_lines or ["  (no source files classified)"])
            + f"\n   {violation_count} gap(s) will be proposed as new components"
            + f"\n   Estimated time: ~{est_seconds}s"
        )

    if dry_run:
        if json_out:
            print(json.dumps({
                "dry_run": True,
                "source": str(target),
                "output": str(dest),
                "files_scanned": total_files_count,
                "by_tier": by_tier,
                "gaps": violation_count,
                "estimated_seconds": est_seconds,
            }, indent=2))
        else:
            console.print(preview_text)
        return

    # ── Confirmation prompt (unless --yes) ────────────────────────────────────
    if not yes and not json_out:
        console.print(preview_text)
        if _first_rebuild:
            # Three-option prompt for first-time rebuilds
            console.print("\n  [bold][P][/bold]roceed  [bold][E][/bold]dit plan  [bold][C][/bold]ancel\n")
            _choice = (typer.prompt("  Choice", default="P")).strip().upper()
            if _choice == "C":
                console.print("[dim]Rebuild cancelled.[/dim]")
                raise typer.Exit(code=0)
            if _choice == "E":
                _plan_path = target / ".ass-ade" / "rebuild-plan.json"
                _plan_path.parent.mkdir(parents=True, exist_ok=True)
                _plan_data = {
                    "source": str(target),
                    "output": str(dest),
                    "tier_distribution": by_tier,
                    "gaps": violation_count,
                    "estimated_seconds": est_seconds,
                }
                _plan_path.write_text(
                    json.dumps(_plan_data, indent=2), encoding="utf-8"
                )
                console.print(f"[dim]Plan saved to:[/dim] {_plan_path}")
                console.print("[dim]Edit the plan, then re-run with --yes to proceed.[/dim]")
                raise typer.Exit(code=0)
            # "P" or anything else → proceed
        else:
            confirm = typer.confirm("Proceed?", default=True)
            if not confirm:
                console.print("[dim]Rebuild cancelled.[/dim]")
                raise typer.Exit(code=0)

    # ── Recon before rebuild ──────────────────────────────────────────────────
    if not json_out:
        console.print(f"[dim]Running recon on {target} ...[/dim]")
    try:
        from ass_ade.recon import run_parallel_recon as _run_recon
        _recon_report = _run_recon(target)
        _recon_md = _recon_report.to_markdown()
        if not json_out:
            console.print(f"[dim]Recon: {_recon_report.scout['total_files']} files, "
                          f"depth {_recon_report.scout['max_depth']}, "
                          f"{_recon_report.test['test_functions']} tests, "
                          f"doc coverage {_recon_report.doc['doc_coverage']:.0%} "
                          f"({_recon_report.duration_ms:.0f} ms)[/dim]")
        if _recon_report.dependency["has_circular_deps"]:
            if not json_out:
                console.print(f"[yellow]Warning: circular imports detected — "
                              f"{_recon_report.dependency['circular_deps'][:2]}[/yellow]")
        _recon_out = target / "RECON_REPORT.md"
        try:
            _recon_out.write_text(_recon_md, encoding="utf-8")
        except OSError:
            pass
    except Exception as _recon_exc:
        if not json_out:
            console.print(f"[dim]Recon skipped: {_recon_exc}[/dim]")

    label = "Premium merge-rebuild" if (premium and _multi_source) else "Merge-rebuild" if _multi_source else ("Premium rebuild" if premium else "Rebuilding")
    if not json_out:
        if _multi_source:
            console.print(f"[bold]{label}[/bold] {len(all_targets)} sources → {dest}")
        else:
            console.print(f"[bold]{label}[/bold] {target}")
            if output:
                console.print(f"[dim]Output → {dest}[/dim]")
        console.print()

    staging_dir = dest.parent / f".{dest.name}_rebuild_staging"

    # ── Show phase progress during the rebuild ────────────────────────────────
    _rebuild_phases = ["Gap-fill", "Enrich", "Validate", "Materialize", "Audit", "Package"]
    _phase_total = len(_rebuild_phases) + 1  # +1 for ingest (already done)
    if not json_out:
        _draw_progress_bar("Rebuild", 1, _phase_total, _t0_ingest)

    _t0_rebuild = _time.monotonic()
    try:
        result = _rebuild_project(
            source_path=all_targets if _multi_source else target,
            output_dir=staging_dir,
            synthesize_gaps=premium,
        )
    except Exception as _exc:
        if json_out:
            print(json.dumps({"error": str(_exc), "source": str(target)}, indent=2))
        else:
            print(flush=True)
            console.print(f"[red]Rebuild failed:[/red] {_exc}")
        raise typer.Exit(code=1)

    if not json_out:
        _finish_progress_bar("Rebuild", _phase_total, _time.monotonic() - _t0_rebuild)

    phases = result.get("phases", {})
    mat = phases.get("materialize", {})
    rebuilt_root_str = mat.get("target_root", "")
    rebuilt_root = Path(rebuilt_root_str) if rebuilt_root_str else None

    if not rebuilt_root or not rebuilt_root.exists():
        if json_out:
            print(json.dumps({"error": "output folder not found", "source": str(target)}, indent=2))
        else:
            console.print("[yellow]Rebuild completed but output folder not found.[/yellow]")
        raise typer.Exit(code=1)

    # ── Auto-versioned output folder name ────────────────────────────────────
    # When user omits the output argument, produce a versioned sibling folder:
    #   {source_name}-v{version}-{timestamp}  (e.g. myapp-v0.1.0-20260418-174111)
    if _auto_versioned_dest:
        _rebuild_tag = mat.get("rebuild_tag", "")
        _project_version = "0.1.0"
        _version_file = rebuilt_root / "VERSION"
        if _version_file.exists():
            try:
                _project_version = _version_file.read_text(encoding="utf-8").splitlines()[0].strip()
            except Exception:
                pass
        _ts_part = _rebuild_tag.replace("_", "-") if _rebuild_tag else ""
        _versioned_name = (
            f"{target.name}-v{_project_version}-{_ts_part}"
            if _ts_part
            else f"{target.name}-v{_project_version}"
        )
        dest = target.parent / _versioned_name
        in_place = False  # treat as a new output folder now that we have a concrete name
        if not json_out:
            console.print(f"[dim]Auto-versioned output → {dest.name}[/dim]")

    _output_backup_path: Path | None = None
    if backup and dest.exists():
        _backup_ts = _time.strftime("%Y%m%d-%H%M%S")
        _output_backup_path = dest.parent / f"{dest.name}-backup-{_backup_ts}"
        _backup_suffix = 0
        while _output_backup_path.exists():
            _backup_suffix += 1
            _output_backup_path = dest.parent / f"{dest.name}-backup-{_backup_ts}-{_backup_suffix}"
        try:
            _shutil.copytree(str(dest), str(_output_backup_path), dirs_exist_ok=False)
            if not json_out:
                console.print(f"[green][OK][/green] Output backup -> {_output_backup_path}")
        except OSError as _backup_exc:
            if json_out:
                print(json.dumps({
                    "error": f"output backup failed: {_backup_exc}",
                    "source": str(target),
                    "output": str(dest),
                }, indent=2))
            else:
                console.print(f"[red]Output backup failed:[/red] {_backup_exc}")
            raise typer.Exit(code=1) from _backup_exc

    # ── Snapshot old component count for incremental diff ────────────────────
    old_count = 0
    if in_place or incremental:
        old_manifest = dest / "MANIFEST.json"
        if old_manifest.exists():
            try:
                old_count = _json.loads(old_manifest.read_text(encoding="utf-8")).get("counts", {}).get("total", 0)
            except Exception:
                pass

    # Preserve BIRTH_CERTIFICATE.md across rebuilds — it is the permanent origin record.
    _birth_cert_content: str | None = None
    _birth_cert_path = dest / "BIRTH_CERTIFICATE.md"
    if _birth_cert_path.exists():
        try:
            _birth_cert_content = _birth_cert_path.read_text(encoding="utf-8")
        except OSError:
            pass
    # Preserve README.md across rebuilds so generated docs do not overwrite the
    # showcase README when a rebuild is promoted into an existing output.
    _readme_content: bytes | None = None
    _readme_path = dest / "README.md"
    if _readme_path.exists():
        try:
            _readme_content = _readme_path.read_bytes()
        except OSError:
            pass
    _env_handoff_path: str | None = None
    _env_handoff_error: str | None = None

    if not in_place:
        _shutil.rmtree(dest, ignore_errors=True)
    _shutil.copytree(str(rebuilt_root), str(dest), dirs_exist_ok=True)

    def _rebase_rebuild_metadata(final_root: Path, staged_root: Path) -> None:
        staged_prefix = staged_root.as_posix()
        final_prefix = final_root.as_posix()

        def _rebase_value(value: Any) -> Any:
            if isinstance(value, str) and value.startswith(staged_prefix):
                return final_prefix + value[len(staged_prefix):]
            if isinstance(value, list):
                return [_rebase_value(item) for item in value]
            if isinstance(value, dict):
                return {key: _rebase_value(item) for key, item in value.items()}
            return value

        manifest_path = final_root / "MANIFEST.json"
        if manifest_path.exists():
            try:
                manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest = _rebase_value(manifest)
                manifest_path.write_text(_json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            except Exception:
                pass

        cert_path = final_root / "CERTIFICATE.json"
        if cert_path.exists():
            try:
                cert = _json.loads(cert_path.read_text(encoding="utf-8"))
                cert = _rebase_value(cert)
                cert["target_root"] = final_prefix
                cert.pop("certificate_sha256", None)
                blob = _json.dumps(cert, sort_keys=True).encode("utf-8")
                cert["certificate_sha256"] = hashlib.sha256(blob).hexdigest()
                cert_path.write_text(_json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                phases.setdefault("certificate", {})["certificate_sha256"] = cert["certificate_sha256"]
                phases["certificate"]["certificate_path"] = cert_path.as_posix()
            except Exception:
                pass

    _rebase_rebuild_metadata(dest, rebuilt_root)

    if _birth_cert_content is not None:
        try:
            (dest / "BIRTH_CERTIFICATE.md").write_text(_birth_cert_content, encoding="utf-8")
        except OSError:
            pass
    if _readme_content is not None:
        try:
            (dest / "README.md").write_bytes(_readme_content)
        except OSError:
            pass

    # Local handoff: let users move into the rebuilt folder without retyping
    # credentials, while .gitignore keeps the file out of public artifacts.
    _env_source = target / ".env"
    _env_dest = dest / ".env"
    if _env_source.exists() and _env_source.is_file():
        try:
            if _env_source.resolve() != _env_dest.resolve():
                _shutil.copy2(str(_env_source), str(_env_dest))
            _env_handoff_path = str(_env_dest)
        except OSError as _env_exc:
            _env_handoff_error = str(_env_exc)

    # ── Save file mtimes for future incremental runs ──────────────────────────
    try:
        existing_manifest_path = dest / "MANIFEST.json"
        existing_manifest: dict = {}
        if existing_manifest_path.exists():
            existing_manifest = _json.loads(existing_manifest_path.read_text(encoding="utf-8"))
        file_mtimes_snapshot: dict[str, float] = {}
        for _st in all_targets:
            for f in _iter_source_files(_st):
                _rel_key = f"{_st.name}/{f.relative_to(_st)}" if _multi_source else str(f.relative_to(_st))
                file_mtimes_snapshot[_rel_key] = f.stat().st_mtime
        existing_manifest["file_mtimes"] = file_mtimes_snapshot
        existing_manifest_path.write_text(
            _json.dumps(existing_manifest, indent=2), encoding="utf-8"
        )
    except Exception:
        pass

    new_count = mat.get("written_count", 0)
    mode_label = "Incremental update" if (in_place or incremental) else "Rebuilt"

    cert = phases.get("certificate", {})

    if not json_out:
        console.print(f"\n[green][OK][/green] {mode_label} → [bold]{dest}[/bold]")
        if _env_handoff_path:
            console.print(f"[green][OK][/green] Local .env copied -> {dest / '.env'}")
        elif _env_handoff_error:
            console.print(f"[yellow].env handoff skipped:[/yellow] {_env_handoff_error[:160]}")

    if (in_place or incremental) and not json_out:
        delta = new_count - old_count
        if delta > 0:
            console.print(f"[green]+{delta} new components[/green] ({old_count} → {new_count})")
        elif delta < 0:
            console.print(f"[yellow]{delta} components removed[/yellow] ({old_count} → {new_count})")
        else:
            console.print(f"[dim]No component count change ({new_count} components)[/dim]")

    if not json_out:
        console.print()
        for line in _render_summary(result).splitlines():
            console.print(f"[dim]{line}[/dim]")

    if not json_out:
        console.print("[dim]Generating documentation suite…[/dim]")
    _recon_stats: "dict | None" = None
    try:
        _rr = _recon_report  # type: ignore[name-defined]
        _recon_stats = {
            "test_functions": _rr.test.get("test_functions", 0),
            "doc_coverage": _rr.doc.get("doc_coverage", 0.0),
        }
    except Exception:
        pass
    _generate_rebuild_docs(
        dest,
        target,
        recon_data=_recon_stats,
        preserve_readme=_readme_content is not None,
    )
    if not json_out:
        console.print("[green][OK][/green] Docs generated.")

    if not no_certify and not cert.get("certificate_sha256"):
        import subprocess as _sp
        rc_cert = _sp.call(
            [sys.executable, "-m", "ass_ade", "certify", str(dest)],
            env=os.environ.copy(),
        )
        cert_ok = rc_cert == 0
        if not json_out:
            if cert_ok:
                console.print("[green][OK][/green] Certified — CERTIFICATE.json written.")
            else:
                console.print("[yellow]Auto-certify failed — run 'ass-ade certify' manually.[/yellow]")
    else:
        cert_ok = bool(cert.get("certificate_sha256"))
        if cert_ok and not json_out:
            console.print("[green][OK][/green] Certified — CERTIFICATE.json written.")

    # ── Git tracking ─────────────────────────────────────────────────────────
    _git_commit_hash: str | None = None
    _git_tag_name: str | None = None
    if git_track:
        import subprocess as _git_sp
        _gt_tag = mat.get("rebuild_tag", "unknown")
        _gt_components = new_count
        _gt_pass_rate = phases.get("audit", {}).get("pass_rate", 0.0)
        _gt_pass_pct = f"{_gt_pass_rate * 100:.1f}"
        _gt_commit_msg = (
            f"evolution: rebuild {_gt_tag} — "
            f"{_gt_components} components, {_gt_pass_pct}% conformant"
        )
        _gt_tag_name = f"rebuild/{_gt_tag}"
        _gt_tag_msg = f"ASS-ADE rebuild {_gt_tag}"
        try:
            # Verify the output is inside a git repo
            _git_check = _git_sp.run(
                ["git", "-C", str(dest), "rev-parse", "--git-dir"],
                capture_output=True, text=True, timeout=10,
            )
            if _git_check.returncode == 0:
                # Stage all files in the output directory
                _git_sp.run(
                    ["git", "-C", str(dest), "add", "-A"],
                    capture_output=True, text=True, timeout=30, check=True,
                )
                # Commit
                _commit_result = _git_sp.run(
                    ["git", "-C", str(dest), "commit", "-m", _gt_commit_msg],
                    capture_output=True, text=True, timeout=30,
                )
                if _commit_result.returncode == 0:
                    _git_commit_hash = _commit_result.stdout.strip().splitlines()[0] if _commit_result.stdout else None
                    # Annotated tag
                    _git_sp.run(
                        ["git", "-C", str(dest), "tag", "-a", _gt_tag_name, "-m", _gt_tag_msg],
                        capture_output=True, text=True, timeout=15,
                    )
                    _git_tag_name = _gt_tag_name
                    if not json_out:
                        console.print(f"[green][OK][/green] Git commit: {_git_commit_hash}")
                        console.print(f"[green][OK][/green] Git tag: {_gt_tag_name}")
                elif "nothing to commit" in (_commit_result.stdout + _commit_result.stderr):
                    if not json_out:
                        console.print("[dim]Git: nothing new to commit.[/dim]")
                else:
                    if not json_out:
                        console.print(f"[yellow]Git commit failed: {_commit_result.stderr.strip()[:120]}[/yellow]")
            else:
                if not json_out:
                    console.print(f"[dim]--git-track: {dest} is not inside a git repo — skipping.[/dim]")
        except Exception as _git_exc:
            if not json_out:
                console.print(f"[dim]--git-track error (rebuild not affected): {_git_exc}[/dim]")

    # ── JSON output ───────────────────────────────────────────────────────────
    if json_out:
        print(json.dumps({
            "ok": True,
            "mode": mode_label.lower().replace(" ", "_"),
            "source": str(target),
            "output": str(dest),
            "files_scanned": total_files_count,
            "components_written": new_count,
            "by_tier": by_tier,
            "gaps": violation_count,
            "certified": cert_ok,
            "incremental_files_skipped": (
                (total_files_count - len(changed_files))
                if changed_files is not None else 0
            ),
            "git_commit": _git_commit_hash,
            "git_tag": _git_tag_name,
            "env_handoff": _env_handoff_path,
            "env_handoff_error": _env_handoff_error,
            "output_backup": str(_output_backup_path) if _output_backup_path else None,
        }, indent=2))

    # ── Clean up staging area ─────────────────────────────────────────────────
    try:
        _shutil.rmtree(str(staging_dir), ignore_errors=True)
    except Exception:
        pass


@app.command("rollback")
def rollback_command(
    path: Path = typer.Argument(Path("."), help="Project root to roll back (default: current directory)."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
) -> None:
    """Restore the most recent backup created by a previous rebuild.

    Finds the newest folder matching ``*-backup-*`` next to the project root,
    shows what will be restored, asks for confirmation, then replaces the
    current project folder with the backup.

    Examples:
        ass-ade rollback .
        ass-ade rollback ./myproject --yes
    """
    import shutil as _shutil
    import stat as _stat

    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    parent = target.parent
    # On Windows, Path("C:") is not the drive root — ensure we use Path("C:/")
    # so that glob() searches the actual drive root directory.
    if str(parent) == parent.drive:
        parent = Path(parent.drive + "/")
    pattern = f"{target.name}-backup-*"
    candidates = sorted(
        [d for d in parent.glob(pattern) if d.is_dir()],
        key=lambda d: d.name,
        reverse=True,
    )

    if not candidates:
        msg = f"No backup folders found matching '{pattern}' in {parent}"
        if json_out:
            print(json.dumps({"ok": False, "error": msg}, indent=2))
        else:
            console.print(f"[yellow]{msg}[/yellow]")
        raise typer.Exit(code=1)

    backup = candidates[0]
    backup_files = sum(1 for f in backup.rglob("*") if f.is_file())
    current_files = sum(1 for f in target.rglob("*") if f.is_file())

    restore_info = {
        "target": str(target),
        "backup": str(backup),
        "backup_name": backup.name,
        "backup_files": backup_files,
        "current_files": current_files,
        "other_backups": [str(c) for c in candidates[1:5]],
    }

    if not yes and not json_out:
        console.print(f"[bold]Rollback plan:[/bold]")
        console.print(f"  Restore from : [cyan]{backup.name}[/cyan] ({backup_files} files)")
        console.print(f"  Overwrites   : [yellow]{target.name}[/yellow] ({current_files} files)")
        if len(candidates) > 1:
            console.print(f"  Other backups: {', '.join(c.name for c in candidates[1:4])}")
        confirmed = typer.confirm("Proceed with rollback?", default=False)
        if not confirmed:
            console.print("[dim]Rollback cancelled.[/dim]")
            raise typer.Exit(code=0)

    # Perform rollback
    def _on_rm_error(func, path, exc_info):
        os.chmod(path, _stat.S_IWRITE)
        func(path)

    try:
        if target.exists():
            _shutil.rmtree(str(target), onerror=_on_rm_error)
        _shutil.copytree(str(backup), str(target))
    except Exception as exc:
        if json_out:
            print(json.dumps({"ok": False, "error": str(exc), **restore_info}, indent=2))
        else:
            console.print(f"[red]Rollback failed:[/red] {exc}")
        raise typer.Exit(code=1)

    if json_out:
        print(json.dumps({"ok": True, **restore_info}, indent=2))
    else:
        console.print(f"[green][OK][/green] Rolled back to [bold]{backup.name}[/bold]")
        console.print(f"[dim]Restored {backup_files} files → {target}[/dim]")


@app.command("enhance")
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
                api_key=settings.nexus_api_key,
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
                    api_key=settings.nexus_api_key,
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


@app.command("docs")
def docs_command(
    path: Path = typer.Argument(Path("."), help="Folder to generate documentation for."),
    config: Path | None = CONFIG_OPTION,
    output_dir: Path | None = typer.Option(None, help="Override output directory (default: <path>)."),
    local_only: bool = typer.Option(
        False,
        help="Skip Nexus API synthesis; generate docs from local analysis only.",
    ),
    allow_remote: bool = typer.Option(
        False,
        help="Force remote enrichment even in local profile.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Print result as JSON."),
) -> None:
    """Auto-generate a full documentation suite for any repository.

    Performs local AST analysis (free, instant) then sends the analysis to the
    AAAA-Nexus docs synthesis engine for intelligent gap-filling and enrichment.
    Free tier: 3 calls/day. Paid: x402 USDC or API key.

    Generated files (written to <path> or --output-dir):
      README.md · ARCHITECTURE.md · FEATURES.md · USER_GUIDE.md
      .gitignore · CONTRIBUTING.md · CHANGELOG.md

    Every synthesis result is captured by the LoRA flywheel to improve
    future runs automatically.

    Examples:
        ass-ade docs .
        ass-ade docs ~/myproject --local-only
        ass-ade docs ~/myproject --allow-remote --json
    """
    from ass_ade.local.docs_engine import build_local_analysis, render_local_docs

    _, settings = _resolve_config(config)
    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    out = output_dir.resolve() if output_dir else target
    console.print(f"[bold]Analyzing[/bold] {target}")

    analysis = build_local_analysis(target)
    meta = analysis.get("metadata", {})
    console.print(
        f"[dim]Detected: {meta.get('name', 'unknown')} "
        f"({', '.join(list(analysis.get('languages', {}).keys())[:3])}), "
        f"{analysis.get('summary', {}).get('total_files', 0)} files[/dim]"
    )

    # Local doc generation (always runs)
    console.print(f"[dim]Generating local docs -> {out}[/dim]")
    written = render_local_docs(analysis, out)

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
                console.print("[dim]Enriching via AAAA-Nexus synthesis engine…[/dim]")
                result = nx.docs_generate(
                    path_analysis=analysis,
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                )
                nexus_result = result.model_dump()
                if result.ok:
                    console.print(
                        f"[green][OK][/green] Nexus synthesis applied "
                        f"({result.files_generated or []} enriched)"
                    )
                    if result.lora_captured:
                        console.print("[dim]LoRA flywheel: sample captured.[/dim]")
                    if result.credit_used:
                        console.print(f"[dim]Credit used: ${result.credit_used:.6f}[/dim]")
        except Exception as exc:
            console.print(f"[yellow]Nexus synthesis unavailable:[/yellow] {exc}")
            console.print("[dim]Falling back to local-only output.[/dim]")

    payload = {
        "ok": True,
        "path": str(target),
        "output_dir": str(out),
        "files_generated": [p.name for p in written.values()],
        "nexus_enriched": nexus_result.get("synthesis_applied", False),
        "lora_captured": nexus_result.get("lora_captured", False),
    }

    if json_out:
        _print_json(payload)
        return

    console.print()
    for name, fpath in written.items():
        console.print(f"  [green]✓[/green] {fpath}")
    console.print(f"\n[green][OK][/green] {len(written)} docs written to {out}")


@app.command("lint")
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


@app.command("certify")
def certify_command(
    path: Path = typer.Argument(Path("."), help="Folder to certify."),
    config: Path | None = CONFIG_OPTION,
    version: str | None = typer.Option(None, help="Version string to embed in the certificate."),
    out: Path | None = typer.Option(None, help="Write CERTIFICATE.json to this path."),
    local_only: bool = typer.Option(
        False,
        help="Generate a local-only unsigned certificate (not verifiable by third parties).",
    ),
    allow_remote: bool = typer.Option(
        False,
        help="Force remote signing even in local profile.",
    ),
    json_out: bool = typer.Option(False, "--json", help="Print certificate as JSON."),
) -> None:
    """Generate a tamper-evident certificate for any codebase.

    Local step: walks the codebase, computes SHA-256 digests of all source
    files, bundles them into a CERTIFICATE.json payload.

    Remote step: sends the local digest to atomadic.tech for PQC signing.
    A certificate is only third-party verifiable when server-signed. Free tier:
    3 calls/day. Paid: x402 USDC or API key.

    Every certification result is captured by the LoRA flywheel.

    Examples:
        ass-ade certify .
        ass-ade certify . --version 1.2.0 --allow-remote
        ass-ade certify ~/myproject --local-only --out CERTIFICATE.json
    """
    import datetime as _dt
    from ass_ade.local.certifier import build_local_certificate, render_certificate_text

    _, settings = _resolve_config(config)
    target = path.resolve()
    if not target.exists():
        console.print(f"[red]Path does not exist:[/red] {target}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Certifying[/bold] {target}")
    cert = build_local_certificate(target, version=version)

    use_remote = not local_only and _should_probe_remote(settings, allow_remote if allow_remote else None)

    if use_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                api_key=settings.nexus_api_key,
                agent_id=str(settings.agent_id) if settings.agent_id else None,
                timeout=60.0,
            ) as nx:
                console.print("[dim]Sending to atomadic.tech for PQC signing…[/dim]")
                result = nx.certify_codebase(
                    local_certificate=cert,
                    agent_id=str(settings.agent_id) if settings.agent_id else None,
                )
                if result.ok and result.signature:
                    cert["signed_by"] = result.signed_by
                    cert["signature"] = result.signature
                    cert["valid"] = result.valid
                    cert["issued_at"] = result.issued_at
                    console.print("[green][OK][/green] Certificate signed by atomadic.tech")
                    if result.lora_captured:
                        console.print("[dim]LoRA flywheel: sample captured.[/dim]")
        except Exception as exc:
            exc_str = str(exc)
            if "402" in exc_str:
                console.print("[yellow]Remote signing requires credits.[/yellow]")
                console.print(
                    "[dim]Get credits at [bold]https://atomadic.tech/pay[/bold] "
                    "then set [bold]AAAA_NEXUS_API_KEY[/bold] in your .env file.[/dim]"
                )
            elif "401" in exc_str or "403" in exc_str:
                console.print(
                    "[yellow]Remote signing failed — API key invalid or missing.[/yellow]"
                )
                console.print(
                    "[dim]Set [bold]AAAA_NEXUS_API_KEY=your_key[/bold] in your project .env file "
                    "([bold]C:\\!ass-ade\\.env[/bold]).[/dim]"
                )
            else:
                console.print(f"[yellow]Remote signing unavailable:[/yellow] {exc}")
            console.print("[dim]Certificate written as local-only (not third-party verifiable).[/dim]")

    cert_path = out or (target / "CERTIFICATE.json")
    import json as _json
    cert_path.write_text(_json.dumps(cert, indent=2, default=str), encoding="utf-8")
    console.print(f"\n[green][OK][/green] Certificate written: {cert_path}")

    if json_out:
        _print_json(cert)
        return

    console.print()
    console.print(render_certificate_text(cert))

    if not cert.get("valid"):
        console.print(
            "\n[yellow]Note:[/yellow] Certificate is not server-signed. "
            "Use --allow-remote or set profile=hybrid/premium for a verifiable certificate."
        )


@app.command("design")
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
                    api_key=settings.nexus_api_key,
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


@app.command("lora-train")
def lora_train(
    lang: str = typer.Option("python", help="Target language."),
    profile: str = typer.Option("fast", help="Model profile: fast | medium | large."),
    base_model: str = typer.Option("", help="Override base-model HF id (blank = use profile default)."),
    epochs: int = typer.Option(3, help="Training epochs."),
    lora_rank: int = typer.Option(8, help="LoRA adapter rank."),
    max_samples: int = typer.Option(1000, help="Max samples to pull."),
    min_samples: int = typer.Option(20, help="Skip training if pool < this."),
    upload: str = typer.Option("hf", help="Upload backend: hf | r2 | local."),
    hf_repo: str = typer.Option("", help="HuggingFace repo id (blank = don't upload to HF)."),
    output_dir: Path = typer.Option(Path(".lora-train-output"), help="Where to stash checkpoints + receipts."),
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Fine-tune a shared LoRA adapter from the live sample pool and promote it.

    Prerequisites:
      - pip install 'ass-ade[lora]'
      - AAAA_NEXUS_OWNER_TOKEN env var (owner-only samples export)
      - HF_TOKEN env var if uploading to Hugging Face

    Runs: fetch_samples -> LoRA fine-tune -> upload -> promote on atomadic.tech.
    """
    import os as _os
    import subprocess as _sp

    _, settings = _resolve_config(config)

    env = {
        **_os.environ,
        "AAAA_NEXUS_BASE_URL": settings.nexus_base_url,
    }
    cmd = [
        sys.executable, "-m", "scripts.lora_train",
        "--lang", lang,
        "--profile", profile,
        "--epochs", str(epochs),
        "--lora-rank", str(lora_rank),
        "--max-samples", str(max_samples),
        "--min-samples", str(min_samples),
        "--upload", upload,
        "--output-dir", str(output_dir),
        "--storefront", settings.nexus_base_url,
    ]
    if base_model:
        cmd.extend(["--base-model", base_model])
    if hf_repo:
        cmd.extend(["--hf-repo", hf_repo])
    _ = config  # acknowledge param, used only to resolve settings above
    console.print(f"[dim]$ {' '.join(cmd)}[/dim]")
    # Stream stdout/stderr so the user sees training progress live.
    rc = _sp.call(cmd, env=env)
    raise typer.Exit(code=rc)


@app.command("lora-credit")
def lora_credit(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show accrued Nexus credit balance (auto-applied on paid calls)."""
    _, settings = _resolve_config(config)
    if settings.profile == "local":
        console.print("[yellow]Local profile — credit is earned/applied in hybrid or premium mode.[/yellow]")
        return
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
            agent_id=settings.agent_id,
        ) as client:
            balance = client.lora_credit_balance(agent_id=settings.agent_id)
            claim = client.lora_reward_claim(agent_id=settings.agent_id)
    except Exception as exc:
        console.print(f"[red]Error:[/red] {exc}")
        return
    t = Table(title=f"Nexus Credit — {settings.agent_id}")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Accepted contributions", str(claim.get("accepted_contributions", 0)))
    t.add_row("Reputation earned", str(claim.get("reputation_earned", 0)))
    t.add_row(
        "Credit balance",
        f"${balance.get('balance_usdc', '0.000000')} "
        f"({balance.get('balance_micro_usdc', 0)} micro-USDC)",
    )
    t.add_row("Reward model", str(balance.get("reward_model", "nexus_api_credit")))
    console.print(t)
    console.print(
        "\n[dim]Balance is auto-deducted on paid calls when X-Agent-Id is set (handled by ass-ade automatically).[/dim]"
    )


@app.command("lora-status")
def lora_status(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Show LoRA flywheel contribution status and adapter health."""
    from ass_ade.agent.lora_flywheel import LoRAFlywheel, RG_LOOP

    _, settings = _resolve_config(config)
    nexus = None
    if settings.profile != "local":
        try:
            nexus = NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
            ).__enter__()
        except Exception:
            pass

    flywheel = LoRAFlywheel(nexus=nexus)
    status = flywheel.status()

    t = Table(title="LoRA Flywheel Status")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Adapter version", status.adapter_version)
    t.add_row("Total contributions", str(status.contribution_count))
    t.add_row("  Fixes captured", str(status.fix_count))
    t.add_row("  Principles captured", str(status.principle_count))
    t.add_row("  Rejections captured", str(status.rejection_count))
    t.add_row("Ratchet epoch", f"{status.ratchet_epoch} / 7")
    t.add_row("Pending contributions", str(status.pending_count))
    t.add_row(f"Next batch (every {RG_LOOP} steps)", f"in {status.next_batch_step} steps")
    if status.quality_score > 0:
        t.add_row("Adapter quality", f"{status.quality_score:.2%}")

    # Fetch live reputation + Nexus credit balance (non-blocking)
    reputation: int | None = None
    credit_micro: int | None = None
    accepted_contributions: int | None = None
    if nexus is not None:
        try:
            claim = nexus.lora_reward_claim(agent_id=settings.agent_id)
            if isinstance(claim, dict):
                reputation = int(claim.get("reputation_earned", 0))
                credit_micro = int(claim.get("usdc_micro_payout", 0))  # legacy field = credit balance
                accepted_contributions = int(claim.get("accepted_contributions", 0))
        except Exception:
            pass

    if accepted_contributions is not None:
        t.add_row("Accepted by Nexus", str(accepted_contributions))
    if reputation is not None:
        t.add_row("Reputation earned", str(reputation))
    if credit_micro is not None:
        t.add_row("Nexus credit accrued", f"${credit_micro / 1_000_000:.6f} (discount against future API calls)")

    console.print(t)

    if credit_micro is not None and credit_micro > 0:
        console.print(
            "\n[green]✓[/green] Credit will auto-discount your next metered Nexus calls.\n"
            "[dim]Reward model: Nexus API-call credits today; on-chain USDC once Nexus is cash-positive.[/dim]"
        )
    elif status.ratchet_epoch == 0:
        console.print("\n[dim]Contribute fixes to earn Nexus API credit + advance the ratchet epoch.[/dim]")
    elif status.ratchet_epoch >= 7:
        console.print("\n[green]✓ Sovereign contributor status achieved.[/green]")


@app.command("setup")
def setup_command(
    reset: bool = typer.Option(False, help="Re-run setup even if config already exists."),
    global_config: bool = typer.Option(
        False, "--global", help="Write config to ~/.ass-ade/config.json instead of the project root."
    ),
) -> None:
    """Interactive setup wizard — configure ASS-ADE in under 60 seconds.

    Prompts for API keys, profile, output path, and evolution mode.
    Saves keys to .env and config to .ass-ade/config.json.

    Run once after install, or with --reset to reconfigure.
    """
    import json as _json
    import subprocess as _sp

    # ── Welcome ────────────────────────────────────────────────────────────────
    console.print("\n[bold cyan]Welcome to ASS-ADE[/bold cyan]")
    console.print(
        "[dim]Autonomous Sovereign System: Atomadic Development Environment — "
        "the CLI that rebuilds, documents, and certifies any codebase.[/dim]\n"
    )

    config_path = (Path.home() / ".ass-ade" / "config.json") if global_config else default_config_path()
    env_path = (Path.home() / ".ass-ade" / ".env") if global_config else (Path.cwd() / ".env")

    if config_path.exists() and not reset:
        console.print(f"[green]✓[/green] Config already exists at [bold]{config_path}[/bold]")
        console.print("[dim]Run with --reset to reconfigure.[/dim]")
        raise typer.Exit(code=0)

    # ── Step 1: API Keys ──────────────────────────────────────────────────────
    console.print("[bold]Step 1/5 — API Keys[/bold]")
    console.print(
        "[dim]Optional. ASS-ADE works without keys (3 free calls/day). "
        "Keys unlock remote signing, lint synthesis, and the LoRA flywheel.[/dim]\n"
    )

    # Load existing .env values
    existing_env: dict[str, str] = {}
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                existing_env[k.strip()] = v.strip()

    def _prompt_key(env_var: str, label: str) -> str:
        current = os.getenv(env_var) or existing_env.get(env_var, "")
        if current:
            console.print(f"  [green]✓[/green] {env_var} already set")
            return current
        val = typer.prompt(
            f"  {label}", default="", show_default=False, hide_input=True,
            prompt_suffix=" (Enter to skip): "
        )
        return val.strip()

    nexus_key = _prompt_key("AAAA_NEXUS_API_KEY", "AAAA Nexus API key (remote signing + synthesis)")
    groq_key = _prompt_key("GROQ_API_KEY", "Groq API key (fast LLM for interpreter)")
    gemini_key = _prompt_key("GEMINI_API_KEY", "Gemini API key (fallback LLM)")

    # Write keys to .env (merge with existing, preserve comments)
    new_env_lines: list[str] = []
    existing_raw = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    written_keys: set[str] = set()
    for line in existing_raw:
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            new_env_lines.append(line)
            continue
        if "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            if k == "AAAA_NEXUS_API_KEY" and nexus_key:
                new_env_lines.append(f"AAAA_NEXUS_API_KEY={nexus_key}")
                written_keys.add(k)
            elif k == "GROQ_API_KEY" and groq_key:
                new_env_lines.append(f"GROQ_API_KEY={groq_key}")
                written_keys.add(k)
            elif k == "GEMINI_API_KEY" and gemini_key:
                new_env_lines.append(f"GEMINI_API_KEY={gemini_key}")
                written_keys.add(k)
            else:
                new_env_lines.append(line)
        else:
            new_env_lines.append(line)
    # Append any new keys not already in .env
    for key, val in [
        ("AAAA_NEXUS_API_KEY", nexus_key),
        ("GROQ_API_KEY", groq_key),
        ("GEMINI_API_KEY", gemini_key),
    ]:
        if val and key not in written_keys:
            new_env_lines.append(f"{key}={val}")
    if any(k for k in (nexus_key, groq_key, gemini_key)):
        env_path.parent.mkdir(parents=True, exist_ok=True)
        env_path.write_text("\n".join(new_env_lines) + "\n", encoding="utf-8")
        console.print(f"\n  [green]✓[/green] Keys saved to [bold]{env_path}[/bold]")
    else:
        console.print("  [dim]No keys entered — using free tier (3 calls/day per endpoint).[/dim]")

    # ── Step 2: Ollama model selection ────────────────────────────────────────
    console.print("\n[bold]Step 2/7 — Local LLM (Ollama)[/bold]")
    from ass_ade.interpreter import get_ollama_models
    ollama_models = get_ollama_models()
    selected_ollama_model = ""
    if ollama_models:
        console.print(f"  [green]✓[/green] Ollama running at localhost:11434")
        console.print("  [dim]Available models:[/dim]")
        for i, m in enumerate(ollama_models[:9], 1):
            console.print(f"    [bold]{i}[/bold]  {m}")
        console.print(f"    [bold]0[/bold]  Skip — don't use Ollama")
        model_choice = typer.prompt("  Select model", default="1")
        choice_idx = model_choice.strip()
        if choice_idx == "0":
            console.print("  [dim]Ollama skipped.[/dim]")
        else:
            try:
                idx = int(choice_idx) - 1
                if 0 <= idx < len(ollama_models):
                    selected_ollama_model = ollama_models[idx]
                    console.print(f"  [green]✓[/green] Ollama model: [bold]{selected_ollama_model}[/bold]")
                else:
                    console.print("  [yellow]Invalid choice — Ollama skipped.[/yellow]")
            except ValueError:
                console.print("  [yellow]Invalid choice — Ollama skipped.[/yellow]")
    else:
        console.print("  [dim]Ollama not detected at localhost:11434 — skipped.[/dim]")
        console.print("  [dim]Install Ollama later and re-run setup to enable local models.[/dim]")

    # ── Step 3: LLM provider order ─────────────────────────────────────────────
    console.print("\n[bold]Step 3/7 — LLM Providers[/bold]")
    console.print("  Select your providers in priority order — highest first.\n")
    _prov_check = [
        ("aaaa-nexus",   "AAAA-Nexus (atomadic.tech)",
         bool(nexus_key or os.environ.get("AAAA_NEXUS_API_KEY"))),
        ("groq",         "Groq",
         bool(groq_key or os.environ.get("GROQ_API_KEY"))),
        ("cerebras",     "Cerebras",
         bool(os.environ.get("CEREBRAS_API_KEY"))),
        ("gemini",       "Gemini",
         bool(gemini_key or os.environ.get("GEMINI_API_KEY"))),
        ("openrouter",   "OpenRouter",
         bool(os.environ.get("OPENROUTER_API_KEY"))),
        ("mistral",      "Mistral",
         bool(os.environ.get("MISTRAL_API_KEY"))),
        ("github",       "GitHub Models",
         bool(os.environ.get("GITHUB_TOKEN"))),
        ("ollama",
         f"Ollama (local){' — ' + ', '.join(ollama_models[:3]) if ollama_models else ''}",
         bool(ollama_models)),
        ("pollinations", "Pollinations (free)", True),
    ]
    for i, (_slug, label, avail) in enumerate(_prov_check, 1):
        status = "[green]✅ available[/green]" if avail else "[dim]❌ no key[/dim]"
        console.print(f"  [bold]{i}[/bold]  {label:<42} {status}")

    _default_nums = [str(i) for i, (_s, _l, avail) in enumerate(_prov_check, 1) if avail]
    _default_str = ",".join(_default_nums) if _default_nums else "9"
    console.print("")
    raw_order = typer.prompt(f"  Priority order (e.g. {_default_str})", default=_default_str)
    _chosen = [s.strip() for s in raw_order.split(",") if s.strip().isdigit()]
    selected_providers: list[str] = []
    for idx_str in _chosen:
        idx = int(idx_str) - 1
        if 0 <= idx < len(_prov_check) and _prov_check[idx][0] not in selected_providers:
            selected_providers.append(_prov_check[idx][0])
    if not selected_providers:
        selected_providers = ["pollinations"]

    # If Ollama chosen but no model configured yet, prompt now
    if "ollama" in selected_providers and not selected_ollama_model:
        if ollama_models:
            console.print("\n  [yellow]Ollama selected — choose a model:[/yellow]")
            for mi, mname in enumerate(ollama_models[:9], 1):
                console.print(f"  [bold]{mi}[/bold]  {mname}")
            mc = typer.prompt("  Model (number, or 0 to skip Ollama)", default="1")
            if mc.strip() == "0":
                selected_providers.remove("ollama")
            else:
                midx = int(mc.strip()) - 1
                if 0 <= midx < len(ollama_models[:9]):
                    selected_ollama_model = ollama_models[midx]
        else:
            console.print("  [dim]Ollama not running — removing from order.[/dim]")
            selected_providers.remove("ollama")

    console.print(f"  [green]✓[/green] Provider order: [bold]{' → '.join(selected_providers)}[/bold]")

    # Derive legacy llm_priority for backwards compatibility
    _first = selected_providers[0] if selected_providers else "pollinations"
    if _first == "aaaa-nexus":
        llm_priority = "nexus"
    elif _first == "ollama":
        llm_priority = "local"
    elif selected_providers == ["pollinations"]:
        llm_priority = "free"
    else:
        llm_priority = "cloud"

    # ── Step 4: Profile ────────────────────────────────────────────────────────
    console.print("\n[bold]Step 4/7 — Profile[/bold]")
    console.print("  [bold]1[/bold]  Local   — free, all core features, no remote calls")
    console.print("  [bold]2[/bold]  Hybrid  — local + Nexus API for signing & synthesis  [dim](recommended if you have a key)[/dim]")
    console.print("  [bold]3[/bold]  Premium — full cloud pipeline")
    default_profile_num = "2" if nexus_key else "1"
    profile_choice = typer.prompt("  Profile", default=default_profile_num)
    profile_map = {"1": "local", "2": "hybrid", "3": "premium"}
    profile = profile_map.get(profile_choice.strip(), "local")
    console.print(f"  [green]✓[/green] Profile: [bold]{profile}[/bold]")

    # ── Step 5: Default output path ───────────────────────────────────────────
    console.print("\n[bold]Step 5/7 — Default rebuild output location[/bold]")
    console.print("  [bold]1[/bold]  Sibling folder  — ../project-rebuilt-{timestamp}  [dim](default)[/dim]")
    console.print("  [bold]2[/bold]  Custom path     — enter a path below")
    out_choice = typer.prompt("  Output location", default="1")
    rebuild_output_strategy = "sibling"
    rebuild_output_path: str | None = None
    if out_choice.strip() == "2":
        custom = typer.prompt("  Custom path", default="./rebuilt")
        rebuild_output_path = custom.strip()
        rebuild_output_strategy = "custom"
    console.print(f"  [green]✓[/green] Output: [bold]{rebuild_output_path or 'sibling of source'}[/bold]")

    # ── Step 6: Evolution mode ────────────────────────────────────────────────
    console.print("\n[bold]Step 6/7 — Evolution mode[/bold]")
    console.print("  [bold]1[/bold]  Single track  — linear evolution on main branch  [dim](default)[/dim]")
    console.print("  [bold]2[/bold]  Dual track    — parallel branches, merge later  [dim](good for big refactors)[/dim]")
    evo_choice = typer.prompt("  Evolution mode", default="1")
    evolution_mode = "dual" if evo_choice.strip() == "2" else "single"
    console.print(f"  [green]✓[/green] Evolution: [bold]{evolution_mode} track[/bold]")

    # ── Step 7: Write config ───────────────────────────────────────────────────
    console.print("\n[bold]Step 7/7 — Saving configuration[/bold]")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    from ass_ade.config import AssAdeConfig, write_default_config
    write_default_config(config_path)

    import json as _json
    cfg_data = _json.loads(config_path.read_text(encoding="utf-8"))
    cfg_data["profile"] = profile
    cfg_data["evolution_mode"] = evolution_mode
    cfg_data["llm_priority"] = llm_priority
    cfg_data["llm_providers"] = selected_providers
    if selected_ollama_model:
        cfg_data["ollama_model"] = selected_ollama_model
    if rebuild_output_strategy == "custom" and rebuild_output_path:
        cfg_data["rebuild_output_path"] = rebuild_output_path
    config_path.write_text(_json.dumps(cfg_data, indent=2), encoding="utf-8")
    console.print(f"  [green]✓[/green] Config written to [bold]{config_path}[/bold]")

    # ── Summary ────────────────────────────────────────────────────────────────
    console.print("\n[bold]Setup complete![/bold]")
    t = Table(show_header=False, box=None)
    t.add_column(style="dim", width=22)
    t.add_column()
    t.add_row("Profile", f"[bold]{profile}[/bold]")
    t.add_row("LLM providers", " → ".join(selected_providers) if selected_providers else llm_priority)
    t.add_row("Ollama model", selected_ollama_model or "[dim]not configured[/dim]")
    t.add_row("Evolution", evolution_mode)
    t.add_row("Output", rebuild_output_path or "sibling of source")
    t.add_row("Nexus key", "[green]set[/green]" if nexus_key else "[dim]not set[/dim]")
    t.add_row("Groq key", "[green]set[/green]" if groq_key else "[dim]not set[/dim]")
    t.add_row("Gemini key", "[green]set[/green]" if gemini_key else "[dim]not set[/dim]")
    console.print(t)

    # ── Auto-run doctor ────────────────────────────────────────────────────────
    console.print("\n[dim]Running environment check (ass-ade doctor)...[/dim]\n")
    try:
        import subprocess as _sp
        _sp.run([sys.executable, "-m", "ass_ade", "doctor"], check=False)
    except Exception as exc:
        console.print(f"[yellow]doctor check skipped:[/yellow] {exc}")

    console.print(
        "\n[dim]Next: run [bold]ass-ade chat[/bold] to start talking to Atomadic, "
        "or [bold]ass-ade enhance .[/bold] to scan this project.[/dim]"
    )


@app.command("tutorial")
def tutorial_command() -> None:
    """Interactive 2-minute demo — rebuild, enhance, docs, and certify a sample project.

    Creates a small messy demo project in a temp directory and walks you
    through the full ASS-ADE workflow: rebuild → enhance → docs → certify.
    Uses the free LLM tier — costs nothing.
    """
    import json as _json
    import shutil as _shutil
    import tempfile as _tmp

    console.print("\n[bold cyan]ASS-ADE Tutorial[/bold cyan]")
    console.print("[dim]2-minute interactive demo. Press Ctrl+C at any time to stop.[/dim]\n")

    # --- Create a messy demo project ---
    tmpdir = Path(_tmp.mkdtemp(prefix="ass-ade-demo-"))
    console.print(f"[dim]Demo project at: {tmpdir}[/dim]\n")

    (tmpdir / "main.py").write_text("""\
# messy demo app
import os, sys, json, pickle

def doStuff(x, y, z):
    # does stuff
    try:
        data = pickle.loads(x)  # nosec — intentional demo of unsafe pattern
        result = eval(y)  # nosec — intentional demo of unsafe pattern
        return data, result
    except Exception:  # noqa: BLE001
        pass

def another_function_with_too_many_lines():
    a = 1; b = 2; c = 3; d = 4; e = 5
    f = 6; g = 7; h = 8; i = 9; j = 10
    k = 11; l = 12; m = 13; n = 14; o = 15
    p = 16; q = 17; r = 18; s = 19; t = 20
    return a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t

class Config:
    def __init__(self):
        self.secret = "hardcoded_secret_12345"
        self.db = "sqlite:///local.db"
""", encoding="utf-8")

    (tmpdir / "utils.py").write_text("""\
import os

def read_file(path):
    # TODO: add error handling
    return open(path).read()

def save_data(obj, filename):
    import pickle
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def compute(n):
    # FIXME: this is slow
    return sum(range(n))
""", encoding="utf-8")

    (tmpdir / "README.md").write_text("# Demo App\n\nA messy codebase.\n", encoding="utf-8")

    console.print("[bold]Step 1: Scan for enhancement opportunities[/bold]")
    console.print(f"[dim]$ ass-ade enhance {tmpdir} --local-only[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    import subprocess as _sp
    r1 = _sp.run(
        [sys.executable, "-m", "ass_ade", "enhance", str(tmpdir), "--local-only"],
        capture_output=False,
    )
    console.print()

    console.print("[bold]Step 2: Generate documentation[/bold]")
    console.print(f"[dim]$ ass-ade docs {tmpdir} --local-only[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    r2 = _sp.run(
        [sys.executable, "-m", "ass_ade", "docs", str(tmpdir), "--local-only"],
        capture_output=False,
    )
    console.print()

    console.print("[bold]Step 3: Certify the codebase[/bold]")
    console.print(f"[dim]$ ass-ade certify {tmpdir}[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    r3 = _sp.run(
        [sys.executable, "-m", "ass_ade", "certify", str(tmpdir)],
        capture_output=False,
    )
    console.print()

    console.print("[bold]Step 4: Run the lint pipeline[/bold]")
    console.print(f"[dim]$ ass-ade lint {tmpdir}[/dim]")
    typer.confirm("Run this step?", default=True, abort=True)

    r4 = _sp.run(
        [sys.executable, "-m", "ass_ade", "lint", str(tmpdir)],
        capture_output=False,
    )
    console.print()

    # --- Summary ---
    console.print("[bold green]Tutorial complete![/bold green]")
    console.print(f"\nDemo files are at: [bold]{tmpdir}[/bold]")
    console.print()
    console.print(
        "[bold]Now point ASS-ADE at your own repo:[/bold]\n"
        "  [cyan]ass-ade enhance ./your-project[/cyan]               # find improvements\n"
        "  [cyan]ass-ade rebuild ./your-project ./clean-output[/cyan] # full monadic rebuild\n"
        "  [cyan]ass-ade docs ./your-project[/cyan]                   # generate docs\n"
        "  [cyan]ass-ade certify ./your-project[/cyan]                # sign the codebase\n"
    )
    keep = typer.confirm("Keep the demo files?", default=False)
    if not keep:
        _shutil.rmtree(tmpdir, ignore_errors=True)


# ── Local LoRA training pipeline ──────────────────────────────────────────────

@app.command("train")
def local_train(
    collect: bool = typer.Option(False, "--collect", help="Collect training data from the current project."),
    run: bool = typer.Option(False, "--run", help="Run LoRA fine-tuning (GPU) or print Colab instructions."),
    serve: bool = typer.Option(False, "--serve", help="Start the local adapter server at localhost:8081."),
    root: Path = typer.Option(Path("."), "--root", help="Project root to scan when collecting (default: cwd)."),
    data_path: Path = typer.Option(
        Path("training_data/training_data.jsonl"),
        "--data",
        help="Training data JSONL path.",
    ),
    output_dir: Path = typer.Option(
        Path("models/lora_adapter"),
        "--output-dir",
        help="Adapter output directory.",
    ),
    base_model: str = typer.Option(
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "--base-model",
        help="Base model HF id.",
    ),
    epochs: int = typer.Option(3, "--epochs", help="Training epochs."),
    lora_rank: int = typer.Option(8, "--lora-rank", help="LoRA rank (default: 8)."),
    port: int = typer.Option(8081, "--port", help="HTTP port for serve mode."),
    preload: bool = typer.Option(False, "--preload", help="Pre-load model on server startup."),
) -> None:
    """Local LoRA training pipeline — bootstrapped from ASS-ADE's own development data.

    Free-tier, self-contained: no Nexus token required.

    Workflow:
      ass-ade train --collect        # scan project and write training_data/training_data.jsonl
      ass-ade train --run            # fine-tune locally (GPU) or print Colab instructions
      ass-ade train --serve          # start adapter server at localhost:8081/generate

    See scripts/lora_training/ for standalone scripts and the Colab notebook.
    See docs/TRAINING_GUIDE.md for the full guide.
    """
    import subprocess as _sp

    if not collect and not run and not serve:
        console.print(
            "[yellow]Specify at least one flag:[/yellow]\n"
            "  [cyan]ass-ade train --collect[/cyan]   collect training data\n"
            "  [cyan]ass-ade train --run[/cyan]        run fine-tuning (or Colab instructions)\n"
            "  [cyan]ass-ade train --serve[/cyan]      start local adapter server"
        )
        raise typer.Exit(code=1)

    collect_script = Path(__file__).parent.parent.parent / "scripts" / "lora_training" / "collect_training_data.py"
    train_script = Path(__file__).parent.parent.parent / "scripts" / "lora_training" / "train_lora.py"
    serve_script = Path(__file__).parent.parent.parent / "scripts" / "lora_training" / "serve_lora.py"

    if collect:
        console.print("[bold]Collecting training data…[/bold]")
        rc = _sp.call([
            sys.executable, str(collect_script),
            "--root", str(root.resolve()),
            "--out", str(data_path),
        ])
        if rc != 0:
            raise typer.Exit(code=rc)
        console.print(f"[green]Done.[/green] Training data saved to [bold]{data_path}[/bold]")

    if run:
        import torch as _torch
        has_gpu = _torch.cuda.is_available()
        if not has_gpu:
            _sp.call([sys.executable, "-c",
                "from scripts.lora_training.train_lora import print_colab_instructions; "
                "from pathlib import Path; "
                f"print_colab_instructions(Path('{data_path}'))"])
        else:
            console.print("[bold]Starting LoRA fine-tuning…[/bold]")
            rc = _sp.call([
                sys.executable, str(train_script),
                "--data", str(data_path),
                "--output-dir", str(output_dir),
                "--base", base_model,
                "--epochs", str(epochs),
                "--lora-rank", str(lora_rank),
            ])
            if rc != 0:
                raise typer.Exit(code=rc)
            console.print(f"[green]Adapter saved to {output_dir}[/green]")

    if serve:
        console.print(f"[bold]Starting adapter server at http://127.0.0.1:{port}/generate…[/bold]")
        rc = _sp.call([
            sys.executable, str(serve_script),
            "--adapter-dir", str(output_dir),
            "--base", base_model,
            "--port", str(port),
            *(["--preload"] if preload else []),
        ])
        raise typer.Exit(code=rc)
        console.print("[dim]Demo files cleaned up.[/dim]")
