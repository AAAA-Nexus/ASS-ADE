"""Tier a1 — assimilated function 'build_gap_fill_plan'

Assimilated from: rebuild/gap_filler.py:279-345
"""

from __future__ import annotations


# --- assimilated symbol ---
def build_gap_fill_plan(
    root_reports: list[dict[str, Any]],
    blueprints: list[dict[str, Any]] | None = None,
    registry: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a full gap-fill plan from one or more ingestion reports.

    Args:
        root_reports: List of dicts from ``project_ingestor.ingest_project``.
        blueprints:   Optional list of blueprint dicts (used for fulfillment mapping).
        registry:     Optional existing component registry (reduces gap count).
    """
    blueprints = blueprints or []
    registry = registry or []

    all_proposals: list[ProposedComponent] = []
    for rr in root_reports:
        root_id = rr.get("root_id") or Path(rr.get("source_root", "")).name
        gaps = rr.get("gaps") or []
        all_proposals.extend(propose_components(gaps, root_id=root_id))

    dedup: dict[str, ProposedComponent] = {}
    sibling_sources: dict[str, list[dict[str, Any]]] = {}
    for prop in all_proposals:
        incumbent = dedup.get(prop.dedup_key)
        if incumbent is None:
            dedup[prop.dedup_key] = prop
            continue
        if _proposal_sort_key(prop) < _proposal_sort_key(incumbent):
            sibling_sources.setdefault(prop.dedup_key, []).append(incumbent.source_symbol)
            dedup[prop.dedup_key] = prop
            continue
        sibling_sources.setdefault(prop.dedup_key, []).append(prop.source_symbol)

    final_proposals = sorted(dedup.values(), key=_proposal_sort_key)
    fulfillment = assess_blueprint_fulfillment(blueprints, final_proposals, registry)

    total_raw_gaps = sum(len(rr.get("gaps") or []) for rr in root_reports)
    deduped_dropped = len(all_proposals) - len(final_proposals)

    plan: dict[str, Any] = {
        "gap_fill_schema": GAP_FILL_SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "summary": {
            "roots": len(root_reports),
            "raw_gaps": total_raw_gaps,
            "proposals_pre_dedup": len(all_proposals),
            "deduped_dropped": deduped_dropped,
            **_summarize_proposals(final_proposals),
            "blueprints_assessed": len(fulfillment),
            "blueprints_fully_satisfied": sum(1 for f in fulfillment if f.get("fully_satisfied")),
        },
        "blueprint_fulfillment": fulfillment,
        "proposed_components": [
            _proposal_record(p, sibling_source_count=len(sibling_sources.get(p.dedup_key, [])))
            for p in final_proposals
        ],
    }
    plan["content_digest"] = hashlib.sha256(
        json.dumps(
            plan["proposed_components"],
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode()
    ).hexdigest()[:16]
    return plan

