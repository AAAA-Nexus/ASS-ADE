"""Tier a2 — assimilated method 'Registry._emit'

Assimilated from: registry.py:727-750
"""

from __future__ import annotations


# --- assimilated symbol ---
def _emit(self, kind: str, atom: Atom) -> None:
    if not self._emit_genesis:
        return
    try:
        from ass_ade.sovereign.genesis_log import emit_event

        emit_event(
            phase="binder",
            kind="decision",
            input={
                "op": kind,
                "canonical_name": atom.canonical_name,
            },
            output={
                "sig_fp": atom.sig_fp,
                "version": f"{atom.version_major}.{atom.version_minor}.{atom.version_patch}",
                "languages": sorted(atom.bodies.keys()),
            },
            verdict="success",
            tags=("registry", kind),
            sovereign=False,
        )
    except Exception:
        _LOGGER.debug("registry genesis emit failed", exc_info=True)

