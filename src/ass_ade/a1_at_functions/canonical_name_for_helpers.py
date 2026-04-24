"""Tier a1 — assimilated function 'canonical_name_for'

Assimilated from: rebuild/schema_materializer.py:246-343
"""

from __future__ import annotations


# --- assimilated symbol ---
def canonical_name_for(
    proposal: dict,
    fallback_tier: str,
    *,
    registry_candidates: list[Atom] | None = None,
    reserved_names: set[str] | None = None,
) -> str:
    """Resolve the canonical name for a proposal via CNA — single source of truth.

    Falls back to a deterministic structured id only when CNA hits a naming
    collision or a public-stem rejection. Blocklist file failures remain
    fail-closed. The fallback still respects the `a[0-4].cat.path.leaf`
    shape so filenames stay uniform.
    """
    src_sym = proposal.get("source_symbol") or {}
    language = (src_sym.get("language") or "python").lower()
    if language not in SUPPORTED_LANGUAGES:
        language = "python"

    intent = _intent_from_proposal(proposal, src_sym)
    signature = _signature_from_proposal(proposal, src_sym)

    # Force CNA's tier head to match the proposal's declared tier directory
    # (so an atom routed to `a2_mo_composites/` always gets an `a2.*` id).
    expected_head = (fallback_tier.split("_", 1)[0] if fallback_tier else "a1")
    if expected_head not in _TIER_HEADS:
        expected_head = "a1"

    try:
        name = cna_assign(
            signature,
            intent,
            language,
            candidates=registry_candidates or [],
        )
        head, _, tail = name.partition(".")
        if head in _TIER_HEADS and head != expected_head and tail:
            name = f"{expected_head}.{tail}"
        name = _plan_local_unique_name(name, proposal, fallback_tier, reserved_names)
        _raise_if_registry_conflict(name, registry_candidates)
        return name
    except CanonicalNameCollision as exc:
        if exc.proposed and not exc.conflicting_atoms:
            try:
                name = cna_llm_propose_name(
                    signature,
                    intent,
                    language,
                    list(exc.proposed),
                    context={
                        "fallback_tier": fallback_tier,
                        "proposal_id": proposal.get("id") or proposal.get("canonical_name"),
                        "proposal_name": proposal.get("name") or src_sym.get("name"),
                        "source_path": src_sym.get("path") or "",
                    },
                )
                head, _, tail = name.partition(".")
                if head in _TIER_HEADS and head != expected_head and tail:
                    name = f"{expected_head}.{tail}"
                name = _plan_local_unique_name(name, proposal, fallback_tier, reserved_names)
                _raise_if_registry_conflict(name, registry_candidates)
                return name
            except (
                CanonicalNameCollision,
                LLMProviderUnavailable,
                LLMResponseError,
                SovereignDomainRejected,
                ValueError,
            ):
                pass
    except SovereignDomainRejected:
        pass

    # Deterministic fallback: tier_head + cleaned legacy id, lowered.
    tier_head = (fallback_tier.split("_", 1)[0] if fallback_tier else "a1")
    if tier_head not in _TIER_HEADS:
        tier_head = "a1"
    raw = (proposal.get("canonical_name") or proposal.get("id")
           or src_sym.get("name") or "atom")
    cleaned = _sanitize_public_fallback(str(raw))
    cleaned = re.sub(r"_+", "_", cleaned).strip("_.") or "atom"
    if cleaned[:1].isdigit():
        cleaned = f"a_{cleaned}"
    fallback_name = (
        f"{tier_head}.{cleaned}"
        if cleaned != tier_head and not cleaned.startswith(f"{tier_head}.")
        else cleaned
    )
    if fallback_name == tier_head:
        fallback_name = f"{tier_head}.atom"
    fallback_name = _plan_local_unique_name(
        fallback_name,
        proposal,
        fallback_tier,
        reserved_names,
    )
    _raise_if_registry_conflict(fallback_name, registry_candidates)
    return fallback_name

