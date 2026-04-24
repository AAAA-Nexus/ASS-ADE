"""Tier a4 — `ass-ade harvest` and `ass-ade assistant` CLI subcommands."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated

import typer

from ass_ade.a0_qk_constants.assistant_types import InsightTag, TaskStatus
from ass_ade.a2_mo_composites.personal_assistant import PersonalAssistant
from ass_ade.a3_og_features.harvest import harvest

# ---------------------------------------------------------------------------
# `ass-ade harvest`
# ---------------------------------------------------------------------------
harvest_app = typer.Typer(no_args_is_help=False)


@harvest_app.callback(invoke_without_command=True)
def harvest_cmd(
    paths: Annotated[
        list[Path],
        typer.Argument(help="Directories or files to harvest. Defaults to current directory."),
    ] = [],
    extensions: Annotated[
        str,
        typer.Option(
            "--ext",
            help="Comma-separated file extensions to scan (e.g. .md,.txt,.py).",
        ),
    ] = ".md,.txt,.rst,.py,.ts,.js",
    max_files: Annotated[int, typer.Option("--max", help="File scan limit.")] = 1000,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Extract but don't persist.")] = False,
    output: Annotated[str, typer.Option("--output", "-o", help="json | text")] = "text",
) -> None:
    """Crawl directories for research docs, chat logs, and notes.

    Extracts key insights, deduplicates them, and builds a structured local
    knowledge base at ~/.ass-ade/assistant/.

    Examples:
      ass-ade harvest ~/notes ~/projects/myapp/docs
      ass-ade harvest . --ext .md,.txt --dry-run
    """
    if not paths:
        paths = [Path(".")]
    ext_tuple = tuple(e.strip() if e.strip().startswith(".") else f".{e.strip()}" for e in extensions.split(","))
    result = harvest(paths, extensions=ext_tuple, max_files=max_files, save=not dry_run)
    if output == "json":
        typer.echo(json.dumps(result.to_dict(), indent=2))
    else:
        typer.echo(result.summary_line())
        if result.insights:
            typer.echo("\nTop insights:")
            for ins in result.insights[:10]:
                tag = ins["tag"].upper()[:10].ljust(10)
                typer.echo(f"  [{tag}] {ins['text'][:80]}")
        if result.tasks:
            typer.echo(f"\nExtracted {len(result.tasks)} tasks:")
            for task in result.tasks[:5]:
                typer.echo(f"  ○ {task['title'][:80]}")
        if dry_run:
            typer.echo("\n(dry-run — nothing persisted)")


# ---------------------------------------------------------------------------
# `ass-ade assistant`
# ---------------------------------------------------------------------------
assistant_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "Personal AI chief-of-staff: tasks, insights, email triage, document organization.\n\n"
        "Run `ass-ade harvest <path>` first to populate the knowledge base."
    ),
)


def _pa() -> PersonalAssistant:
    return PersonalAssistant()


@assistant_app.command("status")
def assistant_status(
    json_out: Annotated[bool, typer.Option("--json", help="Output as JSON.")] = False,
) -> None:
    """Show summary: open tasks, insights, pending items."""
    pa = _pa()
    stat = pa.status()
    if json_out:
        typer.echo(json.dumps(stat, indent=2))
        return
    typer.echo("ASS-ADE Personal Assistant Status")
    typer.echo(f"  Base dir     : {stat['base_dir']}")
    typer.echo(f"  Tasks open   : {stat['tasks_open']} / {stat['tasks_total']}")
    typer.echo(f"  Insights     : {stat['insights_total']}")


@assistant_app.command("tasks")
def assistant_tasks(
    status: Annotated[str, typer.Option("--status", "-s", help="open | in_progress | done")] = "open",
    limit: Annotated[int, typer.Option("--limit", "-n")] = 20,
) -> None:
    """Show extracted action items and TODOs from recent sources."""
    try:
        ts = TaskStatus(status)
    except ValueError:
        typer.echo(f"Unknown status {status!r}. Choose: open, in_progress, done", err=True)
        raise typer.Exit(1)
    pa = _pa()
    tasks = pa.list_tasks(ts)[:limit]
    if not tasks:
        typer.echo(f"No {status} tasks. Run `ass-ade harvest` to extract tasks from your files.")
        return
    typer.echo(f"{len(tasks)} {status} tasks:")
    for task in tasks:
        icon = {"open": "○", "in_progress": "◑", "done": "●"}.get(task["status"], "○")
        src = Path(task["source"]).name[:20]
        typer.echo(f"  {icon} [{task['id'][:6]}] {task['title'][:70]}  ({src})")


@assistant_app.command("complete")
def assistant_complete(
    task_id: Annotated[str, typer.Argument(help="Task ID or prefix.")],
) -> None:
    """Mark a task as done."""
    pa = _pa()
    if pa.complete_task(task_id):
        typer.echo(f"Marked done: {task_id}")
    else:
        typer.echo(f"Task not found: {task_id}", err=True)
        raise typer.Exit(1)


@assistant_app.command("insights")
def assistant_insights(
    tag: Annotated[str, typer.Option("--tag", "-t", help="decision | action | question | idea | risk")] = "",
    limit: Annotated[int, typer.Option("--limit", "-n")] = 20,
) -> None:
    """Show extracted research insights from your knowledge base."""
    pa = _pa()
    insights = pa.list_insights(tag or None)[:limit]
    if not insights:
        typer.echo("No insights yet. Run `ass-ade harvest <path>` to extract insights from your docs.")
        return
    typer.echo(f"{len(insights)} insights" + (f" (tag={tag})" if tag else "") + ":")
    for ins in insights:
        t = ins["tag"].upper()[:10].ljust(10)
        src = Path(ins["source"]).name[:20]
        typer.echo(f"  [{t}] {ins['text'][:75]}  ({src})")


@assistant_app.command("triage")
def assistant_triage(
    path: Annotated[Path, typer.Argument(help="File containing email data (JSON array of email objects).")],
) -> None:
    """Auto-classify and prioritize an email export (JSON format).

    Input JSON must be an array of objects with: subject, sender, date, body fields.
    """
    from ass_ade.a1_at_functions.email_scanner import format_email_row, make_email_summary

    if not path.exists():
        typer.echo(f"File not found: {path}", err=True)
        raise typer.Exit(1)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"Invalid JSON: {exc}", err=True)
        raise typer.Exit(1)
    if not isinstance(raw, list):
        typer.echo("Expected a JSON array of email objects.", err=True)
        raise typer.Exit(1)

    summaries = []
    for item in raw:
        try:
            s = make_email_summary(
                subject=item.get("subject", ""),
                sender=item.get("sender", item.get("from", "")),
                date=item.get("date", ""),
                body=item.get("body", item.get("text", "")),
                message_id=item.get("id", item.get("message_id", "")),
            )
            summaries.append(s)
        except Exception:
            continue

    priority_order = {"urgent": 0, "high": 1, "normal": 2, "low": 3, "newsletter": 4}
    summaries.sort(key=lambda s: priority_order.get(s["priority"], 5))

    typer.echo(f"Triaged {len(summaries)} emails:")
    for s in summaries:
        typer.echo("  " + format_email_row(s))
        if s["action_items"]:
            for ai in s["action_items"]:
                typer.echo(f"      → {ai}")


@assistant_app.command("ingest")
def assistant_ingest(
    text: Annotated[str | None, typer.Option("--text", help="Text to ingest directly.")] = None,
    file: Annotated[Path | None, typer.Option("--file", "-f", help="File to ingest.")] = None,
    source: Annotated[str, typer.Option("--source", "-s", help="Label for this source.")] = "manual",
) -> None:
    """Ingest text or a file into the knowledge base, extracting tasks and insights."""
    if text is None and file is None:
        typer.echo("Provide --text or --file.", err=True)
        raise typer.Exit(1)
    body = text or ""
    if file:
        if not file.exists():
            typer.echo(f"File not found: {file}", err=True)
            raise typer.Exit(1)
        body = file.read_text(encoding="utf-8", errors="replace")
        source = source or str(file)
    pa = _pa()
    tasks = pa.ingest_tasks_from_text(body, source)
    insights = pa.ingest_insights_from_text(body, source)
    typer.echo(f"Ingested: {len(tasks)} new tasks, {len(insights)} new insights  (source={source!r})")
