"""Tier a4 — `ass-ade cron` CLI subcommands."""

from __future__ import annotations

from typing import Annotated

import typer

from ass_ade.a1_at_functions.cron_helpers import format_cron_row, next_run_hint
from ass_ade.a3_og_features.cron_service import CronService

app = typer.Typer(
    no_args_is_help=True,
    help=(
        "Schedule recurring dev tasks — lint runs, daily recon, test sweeps.\n\n"
        "Schedule formats: '0 9 * * *' (cron), @daily, @hourly, @weekly, @monthly."
    ),
)


def _svc() -> CronService:
    return CronService()


@app.command("add")
def cron_add(
    name: Annotated[str, typer.Argument(help="Human name for this job.")],
    schedule: Annotated[str, typer.Argument(help="Cron expression or @alias.")],
    command: Annotated[str, typer.Argument(help="Shell command or `ass-ade` subcommand to run.")],
) -> None:
    """Add a new recurring job.

    Examples:
      ass-ade cron add "daily-lint" "@daily" "ass-ade lint ."
      ass-ade cron add "hourly-check" "0 * * * *" "ass-ade doctor --no-remote"
    """
    svc = _svc()
    try:
        job = svc.add(name, schedule, command)
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)
    typer.echo(
        f"Added [{job['id'][:8]}] {job['name']}  schedule={job['schedule']}"
        f"  next={next_run_hint(job['schedule'])}"
    )


@app.command("list")
def cron_list(
    all_: Annotated[bool, typer.Option("--all", "-a", help="Include disabled jobs.")] = False,
) -> None:
    """List scheduled jobs."""
    svc = _svc()
    jobs = svc.list_jobs(all_=all_)
    if not jobs:
        typer.echo("No scheduled jobs. Use `ass-ade cron add` to create one.")
        return
    typer.echo(f"{'  ':2} {'ID':8}  {'NAME':20} {'SCHEDULE':15} {'LAST RUN':12} {'STATUS':10}  COMMAND")
    typer.echo("-" * 80)
    for job in jobs:
        typer.echo(format_cron_row(job))


@app.command("run")
def cron_run(
    job_id: Annotated[str, typer.Argument(help="Job ID or 8-char prefix.")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Show command output.")] = False,
) -> None:
    """Run a job immediately (ignores schedule)."""
    svc = _svc()
    try:
        exit_code, output = svc.run(job_id)
    except (KeyError, ValueError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)
    status = "OK" if exit_code == 0 else f"FAILED (exit {exit_code})"
    typer.echo(f"Run complete: {status}")
    if verbose or exit_code != 0:
        typer.echo(output[:4000])
    raise typer.Exit(exit_code)


@app.command("enable")
def cron_enable(
    job_id: Annotated[str, typer.Argument(help="Job ID or 8-char prefix.")],
) -> None:
    """Enable a disabled job."""
    svc = _svc()
    try:
        job = svc.enable(job_id)
    except (KeyError, ValueError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)
    typer.echo(f"Enabled: [{job['id'][:8]}] {job['name']}")


@app.command("disable")
def cron_disable(
    job_id: Annotated[str, typer.Argument(help="Job ID or 8-char prefix.")],
) -> None:
    """Disable a job (keep it, just don't run)."""
    svc = _svc()
    try:
        job = svc.disable(job_id)
    except (KeyError, ValueError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)
    typer.echo(f"Disabled: [{job['id'][:8]}] {job['name']}")


@app.command("remove")
def cron_remove(
    job_id: Annotated[str, typer.Argument(help="Job ID or 8-char prefix.")],
    force: Annotated[bool, typer.Option("--force", "-f", help="Skip confirmation.")] = False,
) -> None:
    """Remove a scheduled job permanently."""
    svc = _svc()
    try:
        # resolve first for display
        job = svc._resolve(job_id)  # noqa: SLF001
    except (KeyError, ValueError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)
    if not force:
        confirmed = typer.confirm(f"Remove job [{job['id'][:8]}] {job['name']}?")
        if not confirmed:
            raise typer.Abort()
    svc.remove(job_id)
    typer.echo(f"Removed: [{job['id'][:8]}] {job['name']}")
