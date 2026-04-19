# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_full_cycle.py:7
# Component id: at.source.a1_at_functions.full_cycle
from __future__ import annotations

__version__ = "0.1.0"

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
