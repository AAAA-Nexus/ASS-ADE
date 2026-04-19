"""Tier constants for the ASS-ADE rebuild pipeline."""

from __future__ import annotations

TIERS: list[str] = [
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
]

TIER_PREFIX: dict[str, str] = {
    "a0_qk_constants":      "qk",
    "a1_at_functions":      "at",
    "a2_mo_composites":     "mo",
    "a3_og_features":       "og",
    "a4_sy_orchestration":  "sy",
}
