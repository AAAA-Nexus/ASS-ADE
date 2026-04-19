# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_interpreter_chat.py:7
# Component id: at.source.a1_at_functions.interpreter_chat
from __future__ import annotations

__version__ = "0.1.0"

def interpreter_chat(
    working_dir: Path = typer.Option(
        Path("."), "--dir", "-d", help="Working directory for this session."
    ),
) -> None:
    """Start an interactive chat session with Atomadic.

    Speak plainly — casual, technical, or anywhere in between.
    Atomadic derives your intent and dispatches the right command.
    """
    from ass_ade.interpreter import run_interactive
    run_interactive(working_dir=working_dir.resolve())
