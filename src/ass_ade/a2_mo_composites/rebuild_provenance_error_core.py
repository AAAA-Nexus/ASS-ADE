"""Tier a2 — assimilated class 'RebuildProvenanceError'

Assimilated from: rebuild/schema_materializer.py:396-397
"""

from __future__ import annotations


# --- assimilated symbol ---
class RebuildProvenanceError(RuntimeError):
    """A ``source_symbol.path`` violates the declared allow-listed source root."""

