# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_run_interactive.py:7
# Component id: at.source.a1_at_functions.run_interactive
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

    banner = (
        "Atomadic  ·  ASS-ADE interactive mode\n"
        "Speak plainly. I'll figure out the rest.\n"
        f"Working dir: {wdir}   ·   type 'exit' to quit"
    )
    if use_rich and console:
        console.print(f"\n[bold cyan]{banner}[/bold cyan]\n")
    else:
        print(f"\n{banner}\n")

    # Personalised greeting from memory
    greeting = agent.memory.greeting(wdir)
    if greeting:
        if use_rich and console:
            console.print(f"[dim]{greeting}[/dim]\n")
        else:
            print(f"{greeting}\n")

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
