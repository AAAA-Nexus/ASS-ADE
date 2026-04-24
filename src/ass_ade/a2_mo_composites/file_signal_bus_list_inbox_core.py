"""Tier a2 — assimilated method 'FileSignalBus.list_inbox'

Assimilated from: bus.py:127-140
"""

from __future__ import annotations


# --- assimilated symbol ---
def list_inbox(self) -> list[SignalEnvelope]:
    """Return every well-formed signal in the inbox, oldest first."""
    envelopes: list[SignalEnvelope] = []
    for path in sorted(self.inbox_dir.glob("*.md")):
        try:
            envelopes.append(parse_envelope(path.read_text(encoding="utf-8")))
        except (MalformedSignalError, OSError) as e:
            self._append_log({
                "ts": _rfc3339(self._now()),
                "event": "parse_error",
                "path": str(path),
                "error": f"{type(e).__name__}: {e}",
            })
    return envelopes

