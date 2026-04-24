"""Tier a2 — assimilated method 'FileSignalBus.iter_log'

Assimilated from: bus.py:220-224
"""

from __future__ import annotations


# --- assimilated symbol ---
def iter_log(self) -> Iterable[dict]:
    if not self.log_path.exists():
        return iter(())
    with self.log_path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]  # type: ignore[return-value]

