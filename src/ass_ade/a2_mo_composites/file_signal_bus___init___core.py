"""Tier a2 — assimilated method 'FileSignalBus.__init__'

Assimilated from: bus.py:67-77
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(
    self,
    root: Path,
    agent_id: str,
    *,
    now=None,
) -> None:
    self.root = Path(root)
    self.agent_id = agent_id or "anonymous"
    self._now = now or (lambda: _dt.datetime.now(_dt.UTC))
    self._ensure_layout()

