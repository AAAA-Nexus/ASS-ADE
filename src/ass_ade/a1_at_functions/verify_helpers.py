"""Tier a1 — assimilated function 'verify'

Assimilated from: bindings_lock.py:177-194
"""

from __future__ import annotations


# --- assimilated symbol ---
def verify(plan: BindPlan, lock: LockFile) -> bool:
    """Return True iff ``lock`` structurally agrees with ``plan``.

    Does not re-run the scorer; does not re-read the registry. Callers
    that need a deeper re-bind must call the binder and compare the
    resulting plan. This check is the cheap drift gate that
    ``extend``'s Nexus preflight leans on.
    """
    if not isinstance(lock, LockFile):
        return False
    if lock.manifest_fingerprint != plan.manifest_fingerprint:
        return False
    if not _all_entries_wellformed(lock.entries):
        return False
    expected = _plan_entries(plan)
    if _canonical_entries(lock.entries) != _canonical_entries(expected):
        return False
    return True

