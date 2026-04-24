"""Tier a2 — assimilated class 'SovereignLeakError'

Assimilated from: types.py:323-330
"""

from __future__ import annotations


# --- assimilated symbol ---
class SovereignLeakError(EngineError):
    """An atom's source contains a sovereign-leak pattern.

    Raised by `registry.register` before the atom hits disk. The
    message names the matched pattern class but redacts the exact
    match so the error itself doesn't re-leak. Remediation: scrub the
    offending source, re-fingerprint, retry registration.
    """

