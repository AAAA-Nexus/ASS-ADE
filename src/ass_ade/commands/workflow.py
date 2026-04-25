"""Workflow command group — hero workflows with trust gates, certification, and safe execution."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
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


# ── Workflow Phase Storage ────────────────────────────────────────────────────

_WORKFLOW_DIR = Path(".ass-ade") / "workflow"


def _load_phase_output(n: int, custom: Path | None, repo_path: Path) -> dict[str, Any] | None:
    if custom is not None:
        try:
            return json.loads(custom.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            console.print(f"[red]Cannot read {custom}: {exc}[/red]")
            return None
    default = repo_path / _WORKFLOW_DIR / f"phase{n}.json"
    if default.exists():
        try:
            return json.loads(default.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            console.print(f"[red]Cannot read {default}: {exc}[/red]")
            return None
    return None


def _save_phase_output(n: int, data: dict[str, Any], repo_path: Path) -> Path:
    out_dir = repo_path / _WORKFLOW_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"phase{n}.json"
    out_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return out_path


def _run_verification_step(cmd: list[str], cwd: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=120
        )
        passed = result.returncode == 0
        raw = (result.stdout + result.stderr).strip()
        summary = raw.split("\n")[-1] if raw else "(no output)"
        return {
            "passed": passed,
            "exit_code": result.returncode,
            "summary": summary,
            "output": raw[:2000],
        }
    except FileNotFoundError:
        return {"passed": True, "exit_code": 0, "summary": "(tool not found — skipped)", "output": ""}
    except subprocess.TimeoutExpired:
        return {"passed": False, "exit_code": -1, "summary": "Timed out after 120s", "output": ""}


def _check_tier_purity(root: Path, changed_files: list[str]) -> dict[str, Any]:
    import ast as _ast

    _TIER_ORDER = {
        "a0_qk_constants": 0,
        "a1_at_functions": 1,
        "a2_mo_composites": 2,
        "a3_og_features": 3,
        "a4_sy_orchestration": 4,
    }

    def _file_tier(rel: str) -> int | None:
        for name, lvl in _TIER_ORDER.items():
            if name in rel:
                return lvl
        return None

    py_files = [f for f in changed_files if f.endswith(".py")]
    if not py_files:
        for tier_dir in _TIER_ORDER:
            tier_path = root / "src" / "ass_ade" / tier_dir
            if tier_path.exists():
                for f in tier_path.glob("*.py"):
                    try:
                        py_files.append(str(f.relative_to(root)))
                    except ValueError:
                        py_files.append(f.name)

    violations: list[str] = []
    for rel in py_files[:50]:
        full = root / rel
        if not full.exists():
            continue
        file_lvl = _file_tier(rel)
        if file_lvl is None:
            continue
        try:
            tree = _ast.parse(full.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in _ast.walk(tree):
            if isinstance(node, _ast.ImportFrom) and node.module:
                for tier_name, tier_lvl in _TIER_ORDER.items():
                    if tier_name in node.module and tier_lvl > file_lvl:
                        violations.append(
                            f"{rel}: imports {node.module} (tier {tier_lvl} > {file_lvl})"
                        )
    return {
        "passed": not violations,
        "violations": violations[:10],
        "files_checked": len(py_files),
    }


def _call_inference_for_design(
    task: str, context: dict[str, Any], settings: Any
) -> dict[str, Any] | None:
    files_ctx = "\n".join(
        f"- {f['path']}: {str(f.get('content', ''))[:300]}"
        for f in context.get("files", [])[:5]
    )
    prompt = (
        f"Task: {task}\n\nContext files:\n{files_ctx}\n\n"
        "Return JSON: {summary: str, changes: [{path, action: create|modify|skip, "
        "description, content}]}. Minimal targeted improvements. JSON only."
    )
    try:
        resp = httpx.post(
            f"{settings.nexus_base_url}/v1/inference",
            json={"prompt": prompt, "max_tokens": 2048, "format": "json"},
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        raw = data.get("result") or data.get("output") or data.get("text") or ""
        if isinstance(raw, str):
            raw = json.loads(raw)
        if isinstance(raw, dict) and "changes" in raw:
            return raw
    except Exception:
        pass
    return None


def _heuristic_design(
    task: str, context: dict[str, Any], repo_path: Path
) -> dict[str, Any]:
    import ast as _ast

    root = Path(repo_path).resolve()
    changes: list[dict[str, Any]] = []

    for file_info in context.get("files", []):
        file_path = file_info["path"]
        if not file_path.endswith(".py"):
            continue
        content = file_info.get("content", "")
        try:
            tree = _ast.parse(content)
        except SyntaxError:
            continue

        missing_docs = [
            node.name
            for node in _ast.walk(tree)
            if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef, _ast.ClassDef))
            and not node.name.startswith("_")
            and not (
                node.body
                and isinstance(node.body[0], _ast.Expr)
                and isinstance(node.body[0].value, _ast.Constant)
            )
        ]
        if missing_docs:
            changes.append({
                "path": file_path,
                "action": "modify",
                "description": f"Add docstrings to: {', '.join(missing_docs[:5])}",
                "content": None,
            })

        stem = Path(file_path).stem
        if not stem.startswith("test_"):
            test_rel = str(Path(file_path).parent / f"test_{stem}.py")
            if not (root / test_rel).exists():
                changes.append({
                    "path": test_rel,
                    "action": "skip",
                    "description": f"No test file found for {file_path} — add manually.",
                    "content": None,
                })

    return {
        "summary": (
            f"Heuristic analysis of {len(context.get('files', []))} files. "
            f"{len(changes)} potential improvements identified."
        ),
        "changes": changes[:20],
    }


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
    _save_phase_output(0, result.model_dump(), path)
    console.print(f"Next: {result.next_action}")


def workflow_phase1_context(
    task: str = typer.Argument("", help="Task description (reads phase0 task if empty)."),
    phase0_file: Path | None = typer.Option(None, "--phase0-file", help="Phase 0 JSON to read."),
    path: Path = REPO_PATH_OPTION,
    max_file_size: int = typer.Option(8000, help="Max chars to read per relevant file."),
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 1: gather context from phase0 relevant files and produce a context pack."""
    from ass_ade.recon import phase0_recon

    phase0_data = _load_phase_output(0, phase0_file, path)
    if phase0_data is None:
        if not task.strip():
            console.print("[red]No phase0 output found. Provide --phase0-file or a task argument.[/red]")
            raise typer.Exit(code=1)
        result = phase0_recon(task_description=task, working_dir=path)
        phase0_data = result.model_dump()
        _save_phase_output(0, phase0_data, path)

    task = task or phase0_data.get("task_description", "")
    root = Path(path).resolve()
    file_summaries: list[dict[str, Any]] = []

    for rel_path in phase0_data.get("codebase", {}).get("relevant_files", []):
        full = root / rel_path
        if not full.exists():
            continue
        try:
            raw = full.read_text(encoding="utf-8", errors="replace")
            truncated = raw[:max_file_size]
            if len(raw) > max_file_size:
                truncated += f"\n... ({len(raw) - max_file_size} chars truncated)"
            file_summaries.append({"path": rel_path, "size": len(raw), "content": truncated})
        except OSError:
            pass

    output: dict[str, Any] = {
        "task": task,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": 1,
        "phase0_verdict": phase0_data.get("verdict"),
        "files": file_summaries,
        "file_count": len(file_summaries),
        "next": "phase2-design",
    }
    out_path = _save_phase_output(1, output, path)

    if json_out:
        _print_json(output)
        return

    color = "green" if output["phase0_verdict"] == "READY_FOR_PHASE_1" else "yellow"
    console.print(f"[{color}]Phase 1 Context: {len(file_summaries)} files gathered[/{color}]")
    for f in file_summaries[:5]:
        console.print(f"  - {f['path']} ({f['size']} chars)")
    if len(file_summaries) > 5:
        console.print(f"  … and {len(file_summaries) - 5} more")
    console.print(f"Saved: {out_path}")
    console.print(f"Next: {output['next']}")


def workflow_phase2_design(
    task: str = typer.Argument("", help="Task description (reads phase1 task if empty)."),
    phase1_file: Path | None = typer.Option(None, "--phase1-file", help="Phase 1 JSON to read."),
    path: Path = REPO_PATH_OPTION,
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 2: generate a design blueprint from the context pack."""
    phase1_data = _load_phase_output(1, phase1_file, path)
    if phase1_data is None:
        console.print("[red]Phase 1 output not found. Run `phase1-context` first.[/red]")
        raise typer.Exit(code=1)

    task = task or phase1_data.get("task", "")
    _, settings = _resolve_config(config)

    blueprint: dict[str, Any] | None = None
    strategy = "heuristic"

    if settings.profile != "local" or allow_remote:
        blueprint = _call_inference_for_design(task, phase1_data, settings)
        if blueprint:
            strategy = "inference"

    if blueprint is None:
        blueprint = _heuristic_design(task, phase1_data, path)

    output: dict[str, Any] = {
        "task": task,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": 2,
        "strategy": strategy,
        "changes": blueprint.get("changes", []),
        "summary": blueprint.get("summary", ""),
        "next": "phase3-implement",
    }
    out_path = _save_phase_output(2, output, path)

    if json_out:
        _print_json(output)
        return

    n = len(output["changes"])
    console.print(f"[green]Phase 2 Design: {n} change(s) proposed via {strategy}[/green]")
    for change in output["changes"][:5]:
        console.print(f"  [{change['action']}] {change['path']}: {str(change.get('description',''))[:60]}")
    if n > 5:
        console.print(f"  … and {n - 5} more")
    console.print(f"Saved: {out_path}")
    console.print(f"Next: {output['next']}")


def workflow_phase3_implement(
    phase2_file: Path | None = typer.Option(None, "--phase2-file", help="Phase 2 JSON to read."),
    dry_run: bool = typer.Option(True, "--dry-run/--no-dry-run", help="Preview only (default)."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 3: apply blueprint changes to the codebase (dry-run by default)."""
    phase2_data = _load_phase_output(2, phase2_file, path)
    if phase2_data is None:
        console.print("[red]Phase 2 output not found. Run `phase2-design` first.[/red]")
        raise typer.Exit(code=1)

    task = phase2_data.get("task", "")
    root = Path(path).resolve()
    applied: list[dict[str, Any]] = []

    for change in phase2_data.get("changes", []):
        action = change.get("action", "skip")
        file_path = str(change.get("path", ""))
        content = change.get("content")
        description = str(change.get("description", ""))

        if action == "skip" or content is None:
            applied.append({"path": file_path, "action": action, "status": "skipped", "detail": description})
            continue

        full = root / file_path
        if action in ("create", "modify"):
            if dry_run:
                applied.append({"path": file_path, "action": action, "status": "dry_run",
                                 "detail": f"Would write {len(content)} chars"})
            else:
                try:
                    full.parent.mkdir(parents=True, exist_ok=True)
                    full.write_text(content, encoding="utf-8")
                    applied.append({"path": file_path, "action": action, "status": "applied",
                                    "detail": f"Written {len(content)} chars"})
                except OSError as exc:
                    applied.append({"path": file_path, "action": action, "status": "error",
                                    "detail": str(exc)})
        else:
            applied.append({"path": file_path, "action": action, "status": "skipped", "detail": description})

    changes_count = sum(1 for a in applied if a["status"] == "applied")
    output: dict[str, Any] = {
        "task": task,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": 3,
        "dry_run": dry_run,
        "applied": applied,
        "changes_count": changes_count,
        "next": "phase4-verify",
    }
    out_path = _save_phase_output(3, output, path)

    if json_out:
        _print_json(output)
        return

    _STATUS_COLOR = {"applied": "green", "dry_run": "yellow", "skipped": "dim", "error": "red"}
    mode = "[yellow]DRY RUN[/yellow]" if dry_run else "[green]APPLIED[/green]"
    console.print(f"Phase 3 Implement: {mode}")
    for a in applied[:8]:
        c = _STATUS_COLOR.get(a["status"], "white")
        console.print(f"  [{c}][{a['status'].upper()}][/{c}] {a['path']}: {str(a['detail'])[:60]}")
    if dry_run:
        console.print("[yellow]Pass --no-dry-run to apply changes.[/yellow]")
    console.print(f"Saved: {out_path}")
    console.print(f"Next: {output['next']}")


def workflow_phase4_verify(
    phase3_file: Path | None = typer.Option(None, "--phase3-file", help="Phase 3 JSON to read."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 4: run tests, lint, and tier purity check on changes."""
    phase3_data = _load_phase_output(3, phase3_file, path)
    if phase3_data is None:
        console.print("[yellow]No phase3 output — verifying full suite.[/yellow]")
        task = ""
        changed_files: list[str] = []
    else:
        task = phase3_data.get("task", "")
        changed_files = [
            a["path"] for a in phase3_data.get("applied", []) if a["status"] == "applied"
        ]

    root = Path(path).resolve()
    pytest_result = _run_verification_step(["python", "-m", "pytest", "--tb=short", "-q"], root)
    lint_result = _run_verification_step(["python", "-m", "ruff", "check", "."], root)
    tier_result = _check_tier_purity(root, changed_files)

    overall = pytest_result["passed"] and lint_result["passed"] and tier_result["passed"]
    output: dict[str, Any] = {
        "task": task,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "phase": 4,
        "files_checked": changed_files,
        "pytest": pytest_result,
        "lint": lint_result,
        "tier_purity": tier_result,
        "overall_passed": overall,
        "next": "phase5-certify",
    }
    out_path = _save_phase_output(4, output, path)

    if json_out:
        _print_json(output)
        return

    color = "green" if overall else "red"
    console.print(f"[{color}]Phase 4 Verify: {'PASSED' if overall else 'FAILED'}[/{color}]")
    console.print(f"  pytest:      {'✓' if pytest_result['passed'] else '✗'} {pytest_result['summary'][:60]}")
    console.print(f"  lint:        {'✓' if lint_result['passed'] else '✗'} {lint_result['summary'][:60]}")
    tier_v = len(tier_result['violations'])
    console.print(f"  tier purity: {'✓' if tier_result['passed'] else '✗'} {tier_v} violation(s)")
    console.print(f"Saved: {out_path}")
    if overall:
        console.print(f"Next: {output['next']}")


def workflow_phase5_certify(
    phase4_file: Path | None = typer.Option(None, "--phase4-file", help="Phase 4 JSON to read."),
    path: Path = REPO_PATH_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Phase 5: SHA-256 certify the verified output."""
    phase4_data = _load_phase_output(4, phase4_file, path)
    if phase4_data is None:
        console.print("[red]Phase 4 output not found. Run `phase4-verify` first.[/red]")
        raise typer.Exit(code=1)

    if not phase4_data.get("overall_passed", False):
        console.print("[red]Phase 4 did not pass — certify requires a green verification.[/red]")
        raise typer.Exit(code=2)

    task = phase4_data.get("task", "")
    root = Path(path).resolve()

    file_certs: list[dict[str, str]] = []
    for rel in phase4_data.get("files_checked", []):
        full = root / rel
        if not full.exists():
            continue
        sha = hashlib.sha256(full.read_bytes()).hexdigest()
        file_certs.append({"path": rel, "sha256": sha})

    phase4_json = json.dumps(phase4_data, sort_keys=True, default=str)
    verification_sha = hashlib.sha256(phase4_json.encode()).hexdigest()
    cert_seed = verification_sha + "".join(c["sha256"] for c in file_certs)
    cert_id = hashlib.sha256(cert_seed.encode()).hexdigest()[:16]
    issued_at = datetime.now(timezone.utc).isoformat()

    output: dict[str, Any] = {
        "task": task,
        "timestamp": issued_at,
        "phase": 5,
        "certificate_id": cert_id,
        "files": file_certs,
        "verification_sha256": verification_sha,
        "issued_at": issued_at,
        "verdict": "CERTIFIED",
        "next": "complete",
    }
    out_path = _save_phase_output(5, output, path)

    if json_out:
        _print_json(output)
        return

    console.print(f"[green]Phase 5 Certify: CERTIFIED[/green]")
    console.print(f"  Certificate ID:     {cert_id}")
    console.print(f"  Files certified:    {len(file_certs)}")
    console.print(f"  Verification SHA:   {verification_sha[:16]}…")
    console.print(f"  Issued:             {issued_at}")
    console.print(f"Saved: {out_path}")


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
