"""Tier a2 — assimilated method 'Registry.__init__'

Assimilated from: registry.py:238-250
"""

from __future__ import annotations


# --- assimilated symbol ---
def __init__(
    self,
    path: Path | None = None,
    *,
    pattern_dir: Path | None = None,
    emit_genesis: bool = True,
):
    self._path = path or _default_registry_path()
    self._pattern_dir = pattern_dir or _leak_pattern_dir()
    self._emit_genesis = emit_genesis
    self._lock = threading.RLock()
    self._rows: dict[str, _Row] = {}
    self._load()

