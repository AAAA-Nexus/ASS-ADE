"""Tier a4 — `ass-ade sessions` CLI subcommands."""

from __future__ import annotations

from typing import Annotated

import typer

from ass_ade.a1_at_functions.sessions_helpers import format_history_row, format_session_row
from ass_ade.a3_og_features.sessions_service import SessionsService

app = typer.Typer(no_args_is_help=True, help="Session management — list, create, history, archive.")


def _svc() -> SessionsService:
    return SessionsService()


@app.command("list")
def sessions_list(
    all_: Annotated[bool, typer.Option("--all", "-a", help="Include archived sessions.")] = False,
    query: Annotated[str, typer.Option("--query", "-q", help="Filter by name or summary.")] = "",
) -> None:
    """List active sessions (or all with --all)."""
    svc = _svc()
    records = svc.list_sessions(include_archived=all_, query=query)
    svc.close()
    if not records:
        typer.echo("No sessions found.")
        return
    typer.echo(f"{'  ':2} {'ID':8}  {'NAME':24} {'UPDATED':10}  SUMMARY")
    typer.echo("-" * 72)
    for rec in records:
        typer.echo(format_session_row(rec))


@app.command("new")
def sessions_new(
    name: Annotated[str, typer.Argument(help="Session name.")],
    model: Annotated[str, typer.Option("--model", "-m", help="LLM model for this session.")] = "default",
) -> None:
    """Create a new chat session."""
    svc = _svc()
    rec = svc.new_session(name, model=model)
    svc.close()
    typer.echo(f"Session created: [{rec['id'][:8]}] {rec['name']}  model={rec['model']}")


@app.command("history")
def sessions_history(
    session_id: Annotated[str, typer.Argument(help="Session ID or 8-char prefix.")],
    limit: Annotated[int, typer.Option("--limit", "-n", help="Max messages to show.")] = 50,
) -> None:
    """Show message history for a session."""
    svc = _svc()
    rec = svc.get_session(session_id)
    if rec is None:
        typer.echo(f"Session not found: {session_id}", err=True)
        raise typer.Exit(1)
    messages = svc.get_history(rec["id"], limit=limit)
    svc.close()
    typer.echo(f"Session [{rec['id'][:8]}] {rec['name']}  —  {len(messages)} messages")
    typer.echo("-" * 72)
    for i, msg in enumerate(messages, 1):
        typer.echo(format_history_row(msg, i))


@app.command("send")
def sessions_send(
    session_id: Annotated[str, typer.Argument(help="Session ID or 8-char prefix.")],
    message: Annotated[str, typer.Option("--message", "-m", help="Message text to append.")],
    role: Annotated[str, typer.Option("--role", "-r", help="'user' or 'assistant'.")] = "user",
) -> None:
    """Append a message to a session (scripting / pipe use)."""
    svc = _svc()
    rec = svc.get_session(session_id)
    if rec is None:
        typer.echo(f"Session not found: {session_id}", err=True)
        raise typer.Exit(1)
    msg = svc.add_message(rec["id"], role, message)
    svc.close()
    typer.echo(f"[{msg['ts'][11:19]}] {role}: {message[:80]}")


@app.command("archive")
def sessions_archive(
    session_id: Annotated[str, typer.Argument(help="Session ID or 8-char prefix.")],
) -> None:
    """Archive a session (hide from default list)."""
    svc = _svc()
    rec = svc.get_session(session_id)
    if rec is None:
        typer.echo(f"Session not found: {session_id}", err=True)
        raise typer.Exit(1)
    svc.archive_session(rec["id"])
    svc.close()
    typer.echo(f"Archived: [{rec['id'][:8]}] {rec['name']}")


@app.command("restore")
def sessions_restore(
    session_id: Annotated[str, typer.Argument(help="Session ID or 8-char prefix.")],
) -> None:
    """Restore an archived session to active."""
    svc = _svc()
    rec = svc.get_session(session_id)
    if rec is None:
        typer.echo(f"Session not found: {session_id}", err=True)
        raise typer.Exit(1)
    svc.restore_session(rec["id"])
    svc.close()
    typer.echo(f"Restored: [{rec['id'][:8]}] {rec['name']}")


@app.command("delete")
def sessions_delete(
    session_id: Annotated[str, typer.Argument(help="Session ID or 8-char prefix.")],
    force: Annotated[bool, typer.Option("--force", "-f", help="Skip confirmation.")] = False,
) -> None:
    """Delete a session permanently."""
    svc = _svc()
    rec = svc.get_session(session_id)
    if rec is None:
        typer.echo(f"Session not found: {session_id}", err=True)
        raise typer.Exit(1)
    if not force:
        confirmed = typer.confirm(f"Delete session [{rec['id'][:8]}] {rec['name']}?")
        if not confirmed:
            raise typer.Abort()
    svc.delete_session(rec["id"])
    svc.close()
    typer.echo(f"Deleted: [{rec['id'][:8]}] {rec['name']}")
