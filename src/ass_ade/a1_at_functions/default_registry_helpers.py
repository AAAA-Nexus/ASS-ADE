"""Tier a1 — assimilated function 'default_registry'

Assimilated from: registry.py:762-773
"""

from __future__ import annotations


# --- assimilated symbol ---
def default_registry() -> Registry:
    """Return the process-global registry singleton.

    The singleton is lazily constructed against ``_default_registry_path``.
    Tests that want an isolated registry construct :class:`Registry`
    directly with an explicit path.
    """
    global _DEFAULT
    with _DEFAULT_LOCK:
        if _DEFAULT is None:
            _DEFAULT = Registry()
        return _DEFAULT

