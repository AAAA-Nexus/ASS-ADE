"""ASS-ADE dashboard launcher — boots the AG-UI server + opens browser."""

from __future__ import annotations

import webbrowser
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console


console = Console()


def ui_command(
    host: Annotated[
        str,
        typer.Option("--host", help="Bind host. Use 0.0.0.0 to expose on LAN."),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option("--port", "-p", help="Bind port."),
    ] = 8765,
    no_browser: Annotated[
        bool,
        typer.Option("--no-browser", help="Skip opening the browser."),
    ] = False,
    working_dir: Annotated[
        Path | None,
        typer.Option(
            "--dir",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Working directory override (defaults to cwd).",
        ),
    ] = None,
    static_dir: Annotated[
        Path | None,
        typer.Option(
            "--static",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Serve a prebuilt SPA (SvelteKit/React) from this directory at /.",
        ),
    ] = None,
    reload: Annotated[
        bool,
        typer.Option("--reload", help="Enable uvicorn auto-reload (dev only)."),
    ] = False,
) -> None:
    """Launch the ASS-ADE dashboard — AG-UI event server + local web UI.

    The dashboard exposes the full Atomadic agent as a set of tabs:
    Chat, Scout, Assimilate (cherry-pick), Memory, Skills, Trust, Projects.

    Frontend (SvelteKit/React/Tauri) subscribes to /events for the live
    AG-UI event stream and calls /commands, /chat, /scout/run, etc.
    """
    try:
        import uvicorn
    except ImportError:
        console.print(
            "[red]UI extras not installed.[/red] "
            "Install with: [bold]pip install 'ass-ade[ui]'[/bold] "
            "or [bold]pip install fastapi uvicorn[/bold]"
        )
        raise typer.Exit(1)

    from ass_ade.a3_og_features.ag_ui_server import build_app

    wdir = working_dir or Path.cwd()
    app = build_app(working_dir=wdir)

    if static_dir is not None:
        try:
            from fastapi.staticfiles import StaticFiles

            app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="spa")
        except Exception as exc:
            console.print(f"[yellow]Could not mount static dir:[/yellow] {exc}")

    url = f"http://{host}:{port}"
    console.print(f"[bold cyan]ASS-ADE Dashboard[/bold cyan] → {url}")
    console.print(f"[dim]Working dir: {wdir}[/dim]")
    console.print(f"[dim]AG-UI events: {url}/events[/dim]")
    console.print(f"[dim]Commands:    {url}/commands[/dim]")
    console.print(f"[dim]Health:      {url}/health[/dim]\n")

    if not no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    uvicorn.run(app, host=host, port=port, log_level="info", reload=reload)
