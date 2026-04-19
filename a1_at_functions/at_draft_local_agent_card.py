# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/a2a/__init__.py:310
# Component id: at.source.ass_ade.local_agent_card
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
