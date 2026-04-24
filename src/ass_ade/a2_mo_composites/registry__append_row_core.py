"""Tier a2 — assimilated method 'Registry._append_row'

Assimilated from: registry.py:307-311
"""

from __future__ import annotations


# --- assimilated symbol ---
def _append_row(self, row: dict[str, Any]) -> None:
    self._path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    with self._path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")

