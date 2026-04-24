"""Tier a2 — assimilated method 'Registry._load'

Assimilated from: registry.py:254-269
"""

from __future__ import annotations


# --- assimilated symbol ---
def _load(self) -> None:
    if not self._path.exists():
        return
    with self._path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                _LOGGER.warning(
                    "registry: skipping malformed JSONL row in %s", self._path
                )
                continue
            self._apply_row(row)

