"""Tier a2 — assimilated method 'FileSignalBus._append_log'

Assimilated from: bus.py:215-218
"""

from __future__ import annotations


# --- assimilated symbol ---
def _append_log(self, event: dict) -> None:
    self.log_path.parent.mkdir(parents=True, exist_ok=True)
    with self.log_path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")

