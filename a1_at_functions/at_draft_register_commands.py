# Extracted from C:/!ass-ade/src/ass_ade/commands/__init__.py:8
# Component id: at.source.ass_ade.register_commands
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
