"""Tier a2 — assimilated method 'Registry._leak_check'

Assimilated from: registry.py:715-725
"""

from __future__ import annotations


# --- assimilated symbol ---
def _leak_check(self, atom: Atom) -> None:
    for language, body in atom.bodies.items():
        if not body.source:
            continue
        hits = scan_source_for_leaks(body.source, pattern_dir=self._pattern_dir)
        if hits:
            joined = ",".join(f"{h.category}:{h.redacted}" for h in hits)
            raise SovereignLeakError(
                f"atom {atom.canonical_name!r} body ({language}) "
                f"contains sovereign leak patterns: {joined}"
            )

