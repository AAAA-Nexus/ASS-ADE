"""Tier a2 — assimilated class 'LockFile'

Assimilated from: types.py:258-270
"""

from __future__ import annotations


# --- assimilated symbol ---
class LockFile:
    """`bindings.lock` ledger content.

    One row per blueprint item in the originating manifest, recording
    which Atom version bound and at which sig_fp. Two runs over the
    same manifest + registry must produce byte-identical LockFile
    serializations (ADR-004 reproducibility).
    """

    manifest_fingerprint: str
    entries: list[LockEntry] = field(default_factory=list)
    tool_version: str = ""
    generated_at_iso: str = ""

