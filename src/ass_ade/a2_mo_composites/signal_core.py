"""Tier a2 — assimilated class 'Signal'

Assimilated from: types.py:37-59
"""

from __future__ import annotations


# --- assimilated symbol ---
class Signal:
    """The logical payload an orchestrator broadcasts to the swarm.

    This is the *input* side. Wire-ready form (with ids, timestamps, digests)
    is ``SignalEnvelope`` produced by ``protocol.render_envelope``.
    """

    priority: Priority
    subject: str
    body: str
    routes: tuple[str, ...] = ("*",)
    ack_required: bool = False
    expires_at: str = ""
    issued_by: str = "orchestrator"

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("Signal.subject must be non-empty")
        if not isinstance(self.priority, Priority):
            raise TypeError("Signal.priority must be a Priority enum value")
        if not self.routes:
            raise ValueError("Signal.routes must contain at least one entry "
                             "(use ('*',) for broadcast to all)")

