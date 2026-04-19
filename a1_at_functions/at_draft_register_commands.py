# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_register_commands.py:7
# Component id: at.source.a1_at_functions.register_commands
from __future__ import annotations

__version__ = "0.1.0"

def register_commands(
    agent_app: typer.Typer,
    a2a_app: typer.Typer,
    workflow_app: typer.Typer,
    providers_app: typer.Typer | None = None,
) -> None:
    """Register all command groups lazily.

    Each submodule is imported only when needed, reducing startup time
    and keeping the main app lightweight.
    """
    from . import agent, a2a, workflow

    agent.register(agent_app)
    a2a.register(a2a_app)
    workflow.register(workflow_app)

    if providers_app is not None:
        from . import providers
        providers.register(providers_app)
