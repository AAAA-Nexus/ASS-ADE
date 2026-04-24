"""Tier a1 — assimilated function 'resolve_plan_canonical_names'

Assimilated from: rebuild/schema_materializer.py:346-368
"""

from __future__ import annotations


# --- assimilated symbol ---
def resolve_plan_canonical_names(
    proposed_components: list[dict[str, Any]],
    *,
    registry_candidates: list[Atom] | None = None,
) -> None:
    """Stamp unique canonical ids onto proposals for one rebuild plan."""

    reserved_names: set[str] = set()
    seen: dict[tuple[str, str, str, str, int], str] = {}
    for proposal in proposed_components:
        identity = _proposal_identity_key(proposal)
        if identity in seen:
            proposal["canonical_name"] = seen[identity]
            continue
        canonical = canonical_name_for(
            proposal,
            fallback_tier=proposal.get("tier") or "a1_at_functions",
            registry_candidates=registry_candidates,
            reserved_names=reserved_names,
        )
        reserved_names.add(canonical)
        proposal["canonical_name"] = canonical
        seen[identity] = canonical

