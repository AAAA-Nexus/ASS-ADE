"""Tier a2 — assimilated method 'SwarmCoordinator.__init__'

Assimilated from: coordinator.py:54-62
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(
    self,
    root: Path,
    agent_id: str,
    *,
    bus: FileSignalBus | None = None,
) -> None:
    self.bus = bus or FileSignalBus(root=root, agent_id=agent_id)
    self._handlers: dict[Priority, list[Handler]] = {p: [] for p in Priority}

