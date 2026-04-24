"""Tier a1 — assimilated function 'reset_default_registry'

Assimilated from: registry.py:776-780
"""

from __future__ import annotations


# --- assimilated symbol ---
def reset_default_registry() -> None:
    """Drop the cached default registry. Tests call this between runs."""
    global _DEFAULT
    with _DEFAULT_LOCK:
        _DEFAULT = None

