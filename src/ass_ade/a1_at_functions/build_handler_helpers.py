"""Tier a1 — assimilated function 'build_handler'

Assimilated from: mock_server.py:87-92
"""

from __future__ import annotations


# --- assimilated symbol ---
def build_handler(manifest: dict) -> type[_Handler]:
    """Return a handler class with the given manifest bound."""
    class BoundHandler(_Handler):
        pass
    BoundHandler.manifest = manifest
    return BoundHandler

