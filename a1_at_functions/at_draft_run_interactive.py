# Extracted from C:/!ass-ade/src/ass_ade/interpreter.py:1714
# Component id: at.source.ass_ade.run_interactive
from __future__ import annotations

__version__ = "0.1.0"

def run_interactive(working_dir: Path | None = None) -> None:
    """Drop into an interactive Atomadic session (REPL)."""
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        console: Console | None = Console()
        use_rich = True
    except ImportError:
        console = None
        use_rich = False

    wdir = working_dir or Path.cwd()
    agent = Atomadic(working_dir=wdir)

    is_first_visit = not bool(agent.memory.user_profile)

    # First-visit setup wizard (non-blocking — user can press Enter through it)
    if is_first_visit:
        _run_setup_wizard(console, use_rich, agent)

    # Lightweight scan (under 2 s) — results cached on agent
    scan = quick_project_scan(wdir)
    agent._startup_scan = scan
    greeting_text, suggestions = _build_startup_greeting(scan, agent.memory, wdir, is_first_visit)
    agent._startup_suggestions = suggestions

    if use_rich and console:
        from rich.markdown import Markdown as _Markdown
        console.print()
        console.print(f"[bold cyan]{greeting_text}[/bold cyan]")
        console.print(f"\n[dim]Working dir: {wdir}   ·   type 'exit' to quit[/dim]\n")
    else:
        print(f"\n{greeting_text}")
        print(f"\nWorking dir: {wdir}   ·   type 'exit' to quit\n")

    while True:
        try:
            user_input = input("you → ").strip()
        except (EOFError, KeyboardInterrupt):
            msg = "\nGoodbye!"
            if use_rich and console:
                console.print(f"[dim]{msg}[/dim]")
            else:
                print(msg)
            break

        if user_input.lower() in {"exit", "quit", "bye", "q"}:
            msg = "Goodbye!"
            if use_rich and console:
                console.print(f"[dim]{msg}[/dim]")
            else:
                print(msg)
            break

        if user_input.lower() in {"help", "?", "what can you do"}:
            desc = agent.describe_self()
            if use_rich and console:
                console.print()
                console.print(Markdown(desc))
                console.print()
            else:
                print(f"\n{desc}\n")
            continue

        if not user_input:
            continue

        response = agent.process(user_input)
        if use_rich and console:
            console.print(f"\n[bold green]Atomadic[/bold green] →")
            console.print(Markdown(response))
            console.print()
        else:
            print(f"\nAtomadic → {response}\n")
