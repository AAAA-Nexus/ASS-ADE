"""Tier a2 — assimilated class 'SovereignConstant'

Assimilated from: types.py:299-311
"""

from __future__ import annotations


# --- assimilated symbol ---
class SovereignConstant:
    """Public handle to a sovereign constant.

    The resolver endpoint returns sealed material; this record only
    carries the names needed to call it. No numeric value is ever
    stored in a `SovereignConstant` instance — that would defeat the
    IP wall.
    """

    public_name: str
    private_name: str
    resolver_endpoint: str
    requires_payment: bool

