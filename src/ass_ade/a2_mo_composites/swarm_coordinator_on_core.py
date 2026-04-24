"""Tier a2 — assimilated method 'SwarmCoordinator.on'

Assimilated from: coordinator.py:64-66
"""

from __future__ import annotations


# --- assimilated symbol ---
def on(self, priority: Priority, handler: Handler) -> None:
    """Register a handler to run when a signal of ``priority`` is delivered."""
    self._handlers[priority].append(handler)

