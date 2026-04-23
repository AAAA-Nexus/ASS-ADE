"""Tier a0 — TypedDicts for per-root assimilate policy (engine-deep consumption)."""

from __future__ import annotations

from typing import TypedDict


class RootPolicy(TypedDict, total=False):
    """Resolved per-root policy used by phase engines (ingest).

    Shape mirrors ``.ass-ade/specs/assimilate-policy.schema.json`` rows after
    defaults are applied by ``a1_at_functions.assimilate_policy_plan``.
    """

    role: str
    license_class: str
    forbid_globs: tuple[str, ...]
    allow_globs: tuple[str, ...] | None
    max_file_bytes: int
    binary_handling: str
