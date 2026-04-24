"""Tier a1 — assimilated function 'promotion_checks'

Assimilated from: rebuild/epiphany_cycle.py:118-135
"""

from __future__ import annotations


# --- assimilated symbol ---
def promotion_checks() -> list[dict[str, str]]:
    return [
        {
            "id": "p1",
            "tool": "named_tests",
            "notes": "At least one named pytest or smoke command recorded and passing.",
        },
        {
            "id": "p2",
            "tool": "trust_gate",
            "notes": "When hybrid/premium profile: run trust_gate before treating output as production-safe.",
        },
        {
            "id": "p3",
            "tool": "certify_output",
            "notes": "Optional certify_output after substantive codegen for audit trail.",
        },
    ]

