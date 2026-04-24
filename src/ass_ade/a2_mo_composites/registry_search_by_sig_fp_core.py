"""Tier a2 — assimilated method 'Registry.search_by_sig_fp'

Assimilated from: registry.py:357-388
"""

from __future__ import annotations


# --- assimilated symbol ---
def search_by_sig_fp(
    self, sig_fp_hex: str, within: float | None = None
) -> list[Atom]:
    """Return atoms whose ``sig_fp`` matches (exact or near).

    When ``within`` is ``None`` only exact ``sig_fp`` matches are
    returned. When provided, it is interpreted as a normalized
    Hamming distance in ``[0, 1]`` over the 64-hex-char fingerprint
    treated as a 256-bit vector: atoms with
    ``hamming_distance / 256 <= within`` match.

    The binder is the one module that should pass ``within``; it
    obtains the acceptable bound via the sovereign oracle so no
    numeric threshold is ever named in registry-internal code.
    """
    with self._lock:
        if within is None:
            return [
                row.atom
                for row in self._rows.values()
                if not row.deprecated and row.atom.sig_fp == sig_fp_hex
            ]
        matches: list[Atom] = []
        target = _hex_to_bits(sig_fp_hex)
        for row in self._rows.values():
            if row.deprecated:
                continue
            distance = _bit_distance(target, _hex_to_bits(row.atom.sig_fp))
            normalized = distance / max(1, len(target))
            if normalized <= within:
                matches.append(row.atom)
        return matches

