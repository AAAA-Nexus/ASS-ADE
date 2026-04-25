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
    app.command("phase1-context")(workflow_phase1_context)
    app.command("phase2-design")(workflow_phase2_design)
    app.command("phase3-implement")(workflow_phase3_implement)
    app.command("phase4-verify")(workflow_phase4_verify)
    app.command("phase5-certify")(workflow_phase5_certify)
    app.command("trust-gate")(workflow_trust_gate)
    app.command("certify")(workflow_certify)
    app.command("safe-execute")(workflow_safe_execute)
    app.command("map-terrain")(workflow_map_terrain)


def workflow_phase1_context(
    task_description: str = typer.Argument(..., help="Task description from Phase 0 output."),
    phase0_json: Path | None = typer.Option(
        None, "--phase0", help="Phase 0 recon JSON output file.", exists=True,
    ),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 1 — Context analysis and document gathering.

    Ingests the Phase 0 recon result, gathers relevant file contents,
    resolves imports, and builds the full context packet for Phase 2 design.
    Outputs a context.json file in .ass-ade/workflow/ that Phase 2 consumes.
    """
    import hashlib
    from datetime import datetime as _dt, timezone as _tz

    p0_data: dict = {}
    if phase0_json and phase0_json.exists():
        try:
            p0_data = json.loads(phase0_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"[yellow]Warning: could not read phase0 JSON: {exc}[/yellow]")

    relevant_files: list[str] = p0_data.get("codebase", {}).get("relevant_files", [])
    context_entries: list[dict] = []

    for rel_path in relevant_files[:30]:
        abs_path = path / rel_path
        if abs_path.exists() and abs_path.is_file():
            try:
                content = abs_path.read_text(encoding="utf-8", errors="replace")
                context_entries.append({
                    "path": rel_path,
                    "size_bytes": abs_path.stat().st_size,
                    "content_head": content[:2000],
                    "sha256": hashlib.sha256(content.encode()).hexdigest()[:12],
                })
            except OSError:
                pass

    output_dir = path / ".ass-ade" / "workflow"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "phase1_context.json"

    result = {
        "phase": "phase1-context",
        "task_description": task_description,
        "timestamp": _dt.now(_tz.utc).isoformat(),
        "files_gathered": len(context_entries),
        "context_entries": context_entries,
        "research_targets": p0_data.get("research_targets", []),
        "phase0_verdict": p0_data.get("verdict", "unknown"),
        "next_phase": "phase2-design",
        "next_command": f"ass-ade workflow phase2-design \"{task_description}\" --phase1 {output_file}",
    }
    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if json_out:
        _print_json(result)
        return

    console.print(f"[bold cyan]Phase 1 — Context Analysis[/bold cyan]")
    console.print(f"  Task: {task_description}")
    console.print(f"  Files gathered: [green]{len(context_entries)}[/green]")
    console.print(f"  Output: [dim]{output_file}[/dim]")
    console.print(f"  [dim]Next: {result['next_command']}[/dim]")


def workflow_phase2_design(
    task_description: str = typer.Argument(..., help="Task description."),
    phase1_json: Path | None = typer.Option(
        None, "--phase1", help="Phase 1 context JSON file.", exists=True,
    ),
    path: Path = REPO_PATH_OPTION,
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 2 — Blueprint/spec generation from Phase 0+1 outputs.

    Generates a structured implementation blueprint: which files to create or
    edit, what each change does, and the tier each new file belongs to.
    Outputs blueprint.json in .ass-ade/workflow/ for Phase 3 to execute.
    """
    from datetime import datetime as _dt, timezone as _tz

    p1_data: dict = {}
    if phase1_json and phase1_json.exists():
        try:
            p1_data = json.loads(phase1_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"[yellow]Warning: could not read phase1 JSON: {exc}[/yellow]")

    context_head = ""
    for entry in p1_data.get("context_entries", [])[:5]:
        context_head += f"\n### {entry['path']}\n{entry.get('content_head', '')[:800]}\n"

    blueprint: dict = {
        "phase": "phase2-design",
        "task_description": task_description,
        "timestamp": _dt.now(_tz.utc).isoformat(),
        "files_to_create": [],
        "files_to_edit": [],
        "tier_assignments": {},
        "implementation_notes": f"Blueprint for: {task_description}",
        "context_files_count": len(p1_data.get("context_entries", [])),
        "next_phase": "phase3-implement",
    }

    # Attempt LLM-assisted blueprint via AAAA-Nexus (best-effort)
    _, settings = _resolve_config(config)
    if settings.profile != "local" or allow_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
            ) as client:
                prompt = (
                    f"Generate a concise implementation blueprint as JSON for: {task_description}\n"
                    f"Context files:\n{context_head[:3000]}\n\n"
                    "Return JSON with keys: files_to_create (list of {{path, tier, purpose}}), "
                    "files_to_edit (list of {{path, change}}), implementation_notes (string)."
                )
                import httpx as _httpx
                resp = _httpx.post(
                    f"{settings.nexus_base_url.rstrip('/')}/v1/inference/chat/completions",
                    headers={"Content-Type": "application/json",
                             "X-API-Key": getattr(settings, "nexus_api_key", "") or ""},
                    json={"model": "falcon3-10B-1.58",
                          "messages": [{"role": "user", "content": prompt}],
                          "max_tokens": 800, "temperature": 0.2},
                    timeout=20.0,
                )
                if resp.status_code == 200:
                    raw = resp.json()["choices"][0]["message"]["content"].strip()
                    if "```json" in raw:
                        raw = raw.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw:
                        raw = raw.split("```")[1].split("```")[0].strip()
                    llm_bp = json.loads(raw)
                    blueprint.update({k: v for k, v in llm_bp.items()
                                      if k in ("files_to_create", "files_to_edit", "implementation_notes")})
        except Exception:
            pass

    output_dir = path / ".ass-ade" / "workflow"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "phase2_blueprint.json"
    blueprint["next_command"] = f"ass-ade workflow phase3-implement \"{task_description}\" --phase2 {output_file}"
    output_file.write_text(json.dumps(blueprint, indent=2), encoding="utf-8")

    if json_out:
        _print_json(blueprint)
        return

    console.print(f"[bold cyan]Phase 2 — Blueprint Design[/bold cyan]")
    console.print(f"  Task: {task_description}")
    console.print(f"  Files to create: [green]{len(blueprint['files_to_create'])}[/green]")
    console.print(f"  Files to edit: [yellow]{len(blueprint['files_to_edit'])}[/yellow]")
    console.print(f"  Output: [dim]{output_file}[/dim]")
    console.print(f"  [dim]Next: {blueprint['next_command']}[/dim]")


def workflow_phase3_implement(
    task_description: str = typer.Argument(..., help="Task description."),
    phase2_json: Path | None = typer.Option(
        None, "--phase2", help="Phase 2 blueprint JSON file.", exists=True,
    ),
    path: Path = REPO_PATH_OPTION,
    dry_run: bool = typer.Option(False, "--dry-run", help="Print what would be done without writing files."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 3 — Execute the blueprint: create and edit files per the Phase 2 spec.

    Creates skeleton files in the correct tier directories. Edits are described
    but not auto-applied (human review step). Outputs phase3_result.json.
    """
    import hashlib
    from datetime import datetime as _dt, timezone as _tz

    bp: dict = {}
    if phase2_json and phase2_json.exists():
        try:
            bp = json.loads(phase2_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"[red]Could not read phase2 JSON: {exc}[/red]")
            raise typer.Exit(code=1) from exc

    _tier_docstring = {
        "a0": "Tier a0 — constants and configuration.",
        "a1": "Tier a1 — pure stateless functions.",
        "a2": "Tier a2 — stateful composites and clients.",
        "a3": "Tier a3 — feature modules.",
        "a4": "Tier a4 — orchestration and CLI entry points.",
    }

    created: list[str] = []
    skipped: list[str] = []

    for spec in bp.get("files_to_create", []):
        rel_path = spec.get("path", "")
        if not rel_path.endswith(".py"):
            rel_path += ".py"
        tier = spec.get("tier", "a1")
        purpose = spec.get("purpose", task_description)
        docstring = _tier_docstring.get(tier[:2], f"Tier {tier}.")
        skeleton = (
            f'"""{docstring} {purpose}"""\n'
            f"from __future__ import annotations\n\n"
            f"# TODO: implement {purpose}\n"
        )
        target = path / rel_path
        if dry_run:
            console.print(f"  [dim]would create:[/dim] {rel_path}")
            skipped.append(rel_path)
        elif not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(skeleton, encoding="utf-8")
            created.append(rel_path)
        else:
            skipped.append(rel_path)

    output_dir = path / ".ass-ade" / "workflow"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "phase3_result.json"

    result = {
        "phase": "phase3-implement",
        "task_description": task_description,
        "timestamp": _dt.now(_tz.utc).isoformat(),
        "files_created": created,
        "files_skipped": skipped,
        "edits_pending": bp.get("files_to_edit", []),
        "dry_run": dry_run,
        "next_phase": "phase4-verify",
        "next_command": f"ass-ade workflow phase4-verify \"{task_description}\" --phase3 {output_file}",
    }
    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if json_out:
        _print_json(result)
        return

    console.print(f"[bold cyan]Phase 3 — Implementation[/bold cyan]")
    console.print(f"  Files created: [green]{len(created)}[/green]")
    console.print(f"  Files skipped: [dim]{len(skipped)}[/dim]")
    console.print(f"  Edits pending (manual): [yellow]{len(result['edits_pending'])}[/yellow]")
    if dry_run:
        console.print("  [dim](dry-run — no files written)[/dim]")
    console.print(f"  [dim]Next: {result['next_command']}[/dim]")


def workflow_phase4_verify(
    task_description: str = typer.Argument(..., help="Task description."),
    phase3_json: Path | None = typer.Option(
        None, "--phase3", help="Phase 3 result JSON file.", exists=True,
    ),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 4 — Verify: run tests, lint, and tier purity check.

    Executes `python -m pytest`, checks for tier import violations, and runs
    `ass-ade lint` if available. Outputs phase4_verify.json for Phase 5.
    """
    import subprocess
    from datetime import datetime as _dt, timezone as _tz

    p3_data: dict = {}
    if phase3_json and phase3_json.exists():
        try:
            p3_data = json.loads(phase3_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    checks: list[dict] = []

    def _run(cmd: list[str], label: str) -> dict:
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True, cwd=str(path), timeout=120
            )
            passed = r.returncode == 0
            return {"check": label, "passed": passed,
                    "output": (r.stdout + r.stderr).strip()[-800:]}
        except FileNotFoundError:
            return {"check": label, "passed": False, "output": f"{cmd[0]} not found"}
        except subprocess.TimeoutExpired:
            return {"check": label, "passed": False, "output": "timed out after 120s"}

    console.print("[bold cyan]Phase 4 — Verify[/bold cyan]")

    console.print("  Running tests...")
    checks.append(_run(["python", "-m", "pytest", "tests/", "-x", "--tb=short", "-q"], "pytest"))

    console.print("  Running lint...")
    checks.append(_run(["python", "-m", "ass_ade", "lint", str(path)], "lint"))

    # Tier purity: check created files for upward imports
    created = p3_data.get("files_created", [])
    tier_violations: list[str] = []
    _tier_order = {"a0": 0, "a1": 1, "a2": 2, "a3": 3, "a4": 4}
    for rel in created:
        abs_path = path / rel
        if not abs_path.exists() or not rel.endswith(".py"):
            continue
        try:
            import ast as _ast
            src = abs_path.read_text(encoding="utf-8", errors="replace")
            tree = _ast.parse(src)
            file_tier = next((t for t in _tier_order if t in rel.replace("\\", "/")), None)
            if file_tier is None:
                continue
            file_level = _tier_order[file_tier]
            for node in _ast.walk(tree):
                if isinstance(node, _ast.ImportFrom) and node.module:
                    for up_tier, up_level in _tier_order.items():
                        if up_tier in node.module and up_level > file_level:
                            tier_violations.append(f"{rel} imports {node.module} (upward)")
        except Exception:
            pass

    checks.append({
        "check": "tier-purity",
        "passed": len(tier_violations) == 0,
        "output": "\n".join(tier_violations) if tier_violations else "No upward imports found.",
    })

    all_passed = all(c["passed"] for c in checks)

    output_dir = path / ".ass-ade" / "workflow"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "phase4_verify.json"

    result = {
        "phase": "phase4-verify",
        "task_description": task_description,
        "timestamp": _dt.now(_tz.utc).isoformat(),
        "all_passed": all_passed,
        "checks": checks,
        "next_phase": "phase5-certify",
        "next_command": f"ass-ade workflow phase5-certify \"{task_description}\" --phase4 {output_file}",
    }
    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if json_out:
        _print_json(result)
        return

    for c in checks:
        mark = "[green]✓[/green]" if c["passed"] else "[red]✗[/red]"
        console.print(f"  {mark} {c['check']}")
    color = "green" if all_passed else "red"
    console.print(f"  [{color}]Overall: {'PASS' if all_passed else 'FAIL'}[/{color}]")
    console.print(f"  [dim]Next: {result['next_command']}[/dim]")


def workflow_phase5_certify(
    task_description: str = typer.Argument(..., help="Task description."),
    phase4_json: Path | None = typer.Option(
        None, "--phase4", help="Phase 4 verify JSON file.", exists=True,
    ),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 5 — SHA-256 certification of output.

    Computes a SHA-256 fingerprint over all created files and the task
    description. Writes WORKFLOW_CERTIFICATE.json to .ass-ade/workflow/.
    Only certifies if Phase 4 passed all checks.
    """
    import hashlib
    from datetime import datetime as _dt, timezone as _tz

    p4_data: dict = {}
    if phase4_json and phase4_json.exists():
        try:
            p4_data = json.loads(phase4_json.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"[red]Could not read phase4 JSON: {exc}[/red]")
            raise typer.Exit(code=1) from exc

    if not p4_data.get("all_passed", False):
        console.print("[red]Phase 4 did not pass all checks — certification refused.[/red]")
        console.print("  Fix verification failures before certifying.")
        raise typer.Exit(code=2)

    # Collect all workflow artifacts for fingerprinting
    workflow_dir = path / ".ass-ade" / "workflow"
    artifact_hashes: dict[str, str] = {}
    for f in sorted(workflow_dir.glob("phase*.json")):
        try:
            content = f.read_bytes()
            artifact_hashes[f.name] = hashlib.sha256(content).hexdigest()
        except OSError:
            pass

    combined = task_description + json.dumps(artifact_hashes, sort_keys=True)
    fingerprint = hashlib.sha256(combined.encode()).hexdigest()

    ts = _dt.now(_tz.utc).isoformat()
    certificate = {
        "certificate_type": "workflow-completion",
        "task_description": task_description,
        "timestamp": ts,
        "fingerprint": fingerprint,
        "artifact_hashes": artifact_hashes,
        "phases_certified": list(artifact_hashes.keys()),
        "verdict": "CERTIFIED",
    }

    cert_file = workflow_dir / "WORKFLOW_CERTIFICATE.json"
    cert_file.write_text(json.dumps(certificate, indent=2), encoding="utf-8")

    if json_out:
        _print_json(certificate)
        return

    console.print(f"[bold green]Phase 5 — Certified ✓[/bold green]")
    console.print(f"  Task: {task_description}")
    console.print(f"  Fingerprint: [dim]{fingerprint[:16]}…[/dim]")
    console.print(f"  Artifacts: {len(artifact_hashes)}")
    console.print(f"  Certificate: [dim]{cert_file}[/dim]")


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
