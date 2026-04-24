"""Tier a2 — assimilated method 'SwarmCoordinator.tick'

Assimilated from: coordinator.py:68-93
"""

from __future__ import annotations


# --- assimilated symbol ---
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

