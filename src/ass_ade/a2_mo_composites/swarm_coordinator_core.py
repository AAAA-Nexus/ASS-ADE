"""Tier a2 — assimilated class 'SwarmCoordinator'

Assimilated from: coordinator.py:51-143
"""

from __future__ import annotations


# --- assimilated symbol ---
class SwarmCoordinator:
    """Composes ``FileSignalBus`` with a handler registry."""

    def __init__(
        self,
        root: Path,
        agent_id: str,
        *,
        bus: FileSignalBus | None = None,
    ) -> None:
        self.bus = bus or FileSignalBus(root=root, agent_id=agent_id)
        self._handlers: dict[Priority, list[Handler]] = {p: [] for p in Priority}

    def on(self, priority: Priority, handler: Handler) -> None:
        """Register a handler to run when a signal of ``priority`` is delivered."""
        self._handlers[priority].append(handler)

    def tick(self) -> TickResult:
        """Pull unread signals, dispatch handlers, and report the outcome."""
        receipts = self.bus.unread()
        halts: list[SignalEnvelope] = []
        reroutes: list[SignalEnvelope] = []
        for receipt in receipts:
            env = receipt.envelope
            for handler in self._handlers.get(env.priority, ()):
                try:
                    handler(env)
                except Exception as e:
                    # A handler bug must not swallow a halt signal.
                    self.bus._append_log({  # type: ignore[attr-defined]
                        "ts": env.issued_at,
                        "event": "handler_error",
                        "agent": self.bus.agent_id,
                        "signal_id": env.signal_id,
                        "error": f"{type(e).__name__}: {e}",
                    })
            if env.priority == Priority.P0_HALT:
                halts.append(env)
            elif env.priority == Priority.P1_REROUTE:
                reroutes.append(env)
        return TickResult(delivered=list(receipts),
                          halt_signals=halts,
                          reroute_signals=reroutes)

    # --- convenience publishers ----------------------------------------------

    def announce(
        self,
        subject: str,
        body: str,
        *,
        routes: Iterable[str] = ("*",),
    ) -> SignalEnvelope:
        return self.bus.broadcast(Signal(
            priority=Priority.P2_INFORM,
            subject=subject,
            body=body,
            routes=tuple(routes),
            issued_by=self.bus.agent_id,
        ))

    def reroute(
        self,
        subject: str,
        body: str,
        *,
        routes: Iterable[str],
        ack_required: bool = True,
    ) -> SignalEnvelope:
        return self.bus.broadcast(Signal(
            priority=Priority.P1_REROUTE,
            subject=subject,
            body=body,
            routes=tuple(routes),
            ack_required=ack_required,
            issued_by=self.bus.agent_id,
        ))

    def halt(
        self,
        subject: str,
        body: str,
        *,
        routes: Iterable[str],
    ) -> SignalEnvelope:
        return self.bus.broadcast(Signal(
            priority=Priority.P0_HALT,
            subject=subject,
            body=body,
            routes=tuple(routes),
            ack_required=True,
            issued_by=self.bus.agent_id,
        ))

