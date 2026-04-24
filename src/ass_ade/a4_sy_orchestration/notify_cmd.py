"""Tier a4 — `ass-ade notify` CLI subcommands."""

from __future__ import annotations

from typing import Annotated

import typer

from ass_ade.a0_qk_constants.notify_types import NotifyChannel, NotifyPayload
from ass_ade.a1_at_functions.notify_helpers import format_notify_preview
from ass_ade.a2_mo_composites.notify_client import NotifyClient

app = typer.Typer(
    no_args_is_help=True,
    help="Send build/lint/deploy notifications to Slack, Discord, or webhook.",
)


def _client() -> NotifyClient:
    return NotifyClient()


@app.command("send")
def notify_send(
    text: Annotated[str, typer.Argument(help="Notification message text.")],
    channel: Annotated[str, typer.Option("--channel", "-c", help="slack | discord | webhook | stdout")] = "stdout",
    title: Annotated[str, typer.Option("--title", "-t", help="Short title.")] = "",
    level: Annotated[str, typer.Option("--level", "-l", help="info | success | warning | error")] = "info",
    source: Annotated[str, typer.Option("--source", "-s", help="Which command emitted this.")] = "ass-ade",
) -> None:
    """Send a notification.

    Examples:
      ass-ade notify send "Lint passed!" --channel slack --level success
      ass-ade notify send "Deploy failed" --channel discord --level error
    """
    try:
        ch = NotifyChannel(channel)
    except ValueError:
        typer.echo(f"Unknown channel {channel!r}. Choose: slack, discord, webhook, stdout", err=True)
        raise typer.Exit(1)
    payload = NotifyPayload(text=text, title=title, level=level, source=source)
    client = _client()
    try:
        client.send(ch, payload)
    except (ValueError, RuntimeError) as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)
    if ch != NotifyChannel.STDOUT:
        typer.echo(f"Sent [{channel}]: {format_notify_preview(payload)}")


@app.command("config")
def notify_config(
    slack: Annotated[str | None, typer.Option("--slack", help="Slack incoming webhook URL.")] = None,
    discord: Annotated[str | None, typer.Option("--discord", help="Discord webhook URL.")] = None,
    webhook: Annotated[str | None, typer.Option("--webhook", help="Generic webhook URL.")] = None,
) -> None:
    """Configure webhook URLs for notification channels."""
    client = _client()
    updated = []
    if slack:
        client.set_webhook(NotifyChannel.SLACK, slack)
        updated.append("slack")
    if discord:
        client.set_webhook(NotifyChannel.DISCORD, discord)
        updated.append("discord")
    if webhook:
        client.set_webhook(NotifyChannel.WEBHOOK, webhook)
        updated.append("webhook")
    if not updated:
        configured = client.configured_channels()
        if configured:
            typer.echo(f"Configured channels: {', '.join(configured)}")
        else:
            typer.echo("No channels configured. Use --slack / --discord / --webhook to set URLs.")
        return
    typer.echo(f"Saved: {', '.join(updated)}")


@app.command("test")
def notify_test(
    channel: Annotated[str, typer.Argument(help="Channel to test: slack | discord | webhook | stdout")] = "stdout",
) -> None:
    """Send a test notification to verify webhook configuration."""
    try:
        ch = NotifyChannel(channel)
    except ValueError:
        typer.echo(f"Unknown channel {channel!r}.", err=True)
        raise typer.Exit(1)
    payload = NotifyPayload(
        text="ASS-ADE notification test — everything is working!",
        title="Test",
        level="success",
        source="notify test",
    )
    client = _client()
    try:
        client.send(ch, payload)
        typer.echo(f"Test notification sent to {channel}.")
    except (ValueError, RuntimeError) as exc:
        typer.echo(f"Test failed: {exc}", err=True)
        raise typer.Exit(1)
