# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_local_agent_card.py:7
# Component id: at.source.a1_at_functions.local_agent_card
from __future__ import annotations

__version__ = "0.1.0"

def local_agent_card(working_dir: str = ".") -> A2AAgentCard:
    """Generate an A2A agent card for this ASS-ADE instance.

    Lists all built-in tool capabilities as A2A skills.
    """
    from ass_ade.tools.registry import default_registry

    registry = default_registry(working_dir)

    skills = [
        A2ASkill(
            id=name,
            name=name,
            description=schema.description,
        )
        for name, schema in zip(registry.list_tools(), registry.schemas())
    ]

    return A2AAgentCard(
        name="ASS-ADE",
        description="Autonomous Sovereign Systems: Atomadic Development Environment — agentic IDE with multi-model support",
        url="",  # local instance
        version=__version__,
        provider=A2AProvider(organization="Atomadic", url="https://atomadic.tech"),
        capabilities=A2ACapabilities(
            streaming=True,
            pushNotifications=False,
            stateTransitionHistory=True,
        ),
        authentication=A2AAuthentication(schemes=["bearer"]),
        skills=skills,
        defaultInputModes=["text/plain", "application/json"],
        defaultOutputModes=["text/plain", "application/json"],
    )
