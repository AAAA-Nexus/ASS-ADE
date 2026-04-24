"""Tier a1 — assimilated function 'write'

Assimilated from: bindings_lock.py:109-134
"""

from __future__ import annotations


# --- assimilated symbol ---
def write(plan: BindPlan, path: Path, *, tool_version: str = "", generated_at_iso: str = "") -> None:
    """Atomically materialize a :class:`BindPlan` as a ``bindings.lock``.

    The lock file on disk holds **only** the minimum state needed to
    reconstruct which atoms are pinned — it is not a full audit log.
    Decision metadata (REUSE vs EXTEND vs REFACTOR vs SYNTHESIZE)
    lives in genesis events, not here.

    Reproducibility contract: given the same ``plan`` (including the
    same ``manifest_fingerprint`` and the same optional
    ``generated_at_iso``/``tool_version`` kwargs), two calls produce
    byte-identical files. Callers that care about cross-invocation
    byte-equality MUST pass a stable ``generated_at_iso`` (e.g.
    derived from the manifest hash) rather than the wall clock.
    """
    if plan.bindings_lock is not None:
        tool_version = tool_version or plan.bindings_lock.tool_version
        generated_at_iso = generated_at_iso or plan.bindings_lock.generated_at_iso
    lock = _plan_to_lock(
        plan,
        tool_version=tool_version,
        generated_at_iso=generated_at_iso,
    )
    payload = _serialize(lock)
    _atomic_write_bytes(path, payload)
    _emit_write_event(plan, lock, path)

