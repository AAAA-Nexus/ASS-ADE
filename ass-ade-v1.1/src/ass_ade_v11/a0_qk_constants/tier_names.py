"""Tier identifiers aligned with ASS-ADE rebuild materialization."""

from __future__ import annotations

TIERS: list[str] = [
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
]

TIER_PREFIX: dict[str, str] = {
    "a0_qk_constants": "a0",
    "a1_at_functions": "a1",
    "a2_mo_composites": "a2",
    "a3_og_features": "a3",
    "a4_sy_orchestration": "a4",
}

PREFIX_TO_TIER: dict[str, str] = {
    **{prefix: tier for tier, prefix in TIER_PREFIX.items()},
    "qk": "a0_qk_constants",
    "at": "a1_at_functions",
    "mo": "a2_mo_composites",
    "og": "a3_og_features",
    "sy": "a4_sy_orchestration",
}

VALID_TIER_DIRS: frozenset[str] = frozenset(TIERS)
