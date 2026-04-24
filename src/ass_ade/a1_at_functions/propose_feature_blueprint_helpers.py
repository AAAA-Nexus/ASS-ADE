"""Tier a1 — assimilated function 'propose_feature_blueprint'

Assimilated from: rebuild/feature.py:155-226
"""

from __future__ import annotations


# --- assimilated symbol ---
def propose_feature_blueprint(
    description: str,
    *,
    feature_name: str | None = None,
    target: Path | None = None,
    base_url: str = DEFAULT_BASE_URL,
    api_key: str | None = None,
    agent_id: str | None = None,
    allow_fallback: bool = False,
) -> dict[str, Any]:
    """Propose a tier-aligned blueprint for ``description``.

    No heuristic fallback: if Nexus is unreachable or returns unusable
    content, :class:`RuntimeError` is raised with the attempted base URL
    so the caller can see exactly what failed. The legacy placeholder
    fallback is retained only for test fixtures; production callers must
    leave ``allow_fallback=False``.
    """
    api_key = api_key or os.environ.get("AAAA_NEXUS_API_KEY")
    agent_id = agent_id or os.environ.get("AAAA_NEXUS_AGENT_ID")

    proposed = _propose_via_nexus(
        description,
        target=target,
        base_url=base_url,
        api_key=api_key,
        agent_id=agent_id,
    )
    source = "nexus"
    if proposed is None:
        if not allow_fallback:
            from ass_ade.engine.rebuild.synthesis import consume_last_nexus_error
            detail = consume_last_nexus_error() or "no detail available"
            raise RuntimeError(
                f"Feature proposal failed against {base_url}. "
                f"Reason: {detail}. Check AAAA_NEXUS_API_KEY and AAAA_NEXUS_BASE_URL."
            )
        proposed = [{
            "name": (_slug(description)[:32] or "feature") + "_entry",
            "tier": "a3_og_features",
            "purpose": description[:160],
            "signature": "def entry(*args, **kwargs) -> None:",
        }]
        source = "fallback"

    feature_slug = _slug(feature_name or description)[:48] or "feature"
    components = [
        {
            "id": _component_id(c),
            "name": _slug(c["name"]),
            "tier": c["tier"],
            "purpose": c.get("purpose", ""),
            "signature": c.get("signature", ""),
        }
        for c in proposed
    ]
    tiers_used = sorted({c["tier"] for c in components})

    return {
        "schema": "AAAA-SPEC-004",
        "blueprint_id": f"bp_{feature_slug}",
        "blueprint_name": feature_name or description[:80],
        "description": description,
        "components": components,
        "tiers": tiers_used,
        "metadata": {
            "generator": "ass-ade/feature",
            "source": source,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "target": str(target) if target else None,
        },
    }

