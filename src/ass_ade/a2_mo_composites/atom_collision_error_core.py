"""Tier a2 — assimilated class 'AtomCollisionError'

Assimilated from: types.py:333-340
"""

from __future__ import annotations


# --- assimilated symbol ---
class AtomCollisionError(EngineError):
    """A registration would break two-fingerprint versioning.

    Specifically: a caller tried to register an atom at a
    `canonical_name` that already exists with a different `sig_fp`
    without requesting a major version bump. The registry surfaces
    the conflict so the caller decides.
    """

