"""Tier a1 — assimilated function 'scan_path'

Assimilated from: rebuild/finish.py:134-144
"""

from __future__ import annotations


# --- assimilated symbol ---
def scan_path(root: Path) -> list[IncompleteFunction]:
    incomplete: list[IncompleteFunction] = []
    if root.is_file() and root.suffix == ".py":
        return scan_file(root)
    for py in sorted(root.rglob("*.py")):
        # Skip test and build artifacts.
        parts = set(py.parts)
        if parts & {"__pycache__", ".venv", "venv", "build", "dist", ".ass-ade"}:
            continue
        incomplete.extend(scan_file(py))
    return incomplete

