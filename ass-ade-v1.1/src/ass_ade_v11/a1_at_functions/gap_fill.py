"""Gap-fill plan from ingestion reports (pure)."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ass_ade_v11.a0_qk_constants.schemas import GAP_FILL_SCHEMA
from ass_ade_v11.a0_qk_constants.tier_names import TIER_PREFIX
from ass_ade_v11.a1_at_functions.registry_fingerprint import (
    fingerprint_gap_proposal,
    fold_registry_token,
)


@dataclass
class ProposedComponent:
    id: str
    tier: str
    kind: str
    name: str
    source_symbol: dict[str, Any]
    product_categories: list[str]
    fulfills_blueprints: list[str] = field(default_factory=list)
    made_of: list[str] = field(default_factory=list)
    description: str = ""
    dedup_key: str = ""
    source_rank: int = 0


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "component"


def _tier_prefix(tier: str) -> str:
    return TIER_PREFIX.get(tier, "a1")


def _normalize_categories(categories: list[str] | None) -> list[str]:
    normalized = sorted({str(c) for c in (categories or []) if str(c)})
    return normalized or ["COR"]


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _dedup_key(tier: str, name: str, categories: list[str]) -> str:
    cat = ",".join(_normalize_categories(categories))
    return f"{tier}|{fold_registry_token(name)}|{cat}"


def _proposal_sort_key(prop: ProposedComponent) -> tuple[str, ...]:
    return (
        prop.dedup_key,
        prop.id,
        prop.tier,
        prop.kind,
        prop.name,
        _stable_json(prop.product_categories),
        _stable_json(prop.made_of),
        _stable_json(prop.source_symbol),
    )


def _should_replace_incumbent(incumbent: ProposedComponent, prop: ProposedComponent) -> bool:
    """Lower ``source_rank`` wins (0 = primary MAP root); tie-break with sort key."""
    if prop.source_rank < incumbent.source_rank:
        return True
    if prop.source_rank > incumbent.source_rank:
        return False
    return _proposal_sort_key(prop) < _proposal_sort_key(incumbent)


def _proposal_record(
    prop: ProposedComponent,
    *,
    sibling_source_count: int = 0,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "id": prop.id,
        "tier": prop.tier,
        "kind": prop.kind,
        "name": prop.name,
        "description": prop.description,
        "made_of": prop.made_of,
        "product_categories": list(prop.product_categories),
        "fulfills_blueprints": sorted(set(prop.fulfills_blueprints)),
        "source_symbol": prop.source_symbol,
        "dedup_key": prop.dedup_key,
        "source_rank": prop.source_rank,
        "sibling_source_count": sibling_source_count,
    }
    rec["fingerprint_sha256"] = fingerprint_gap_proposal(rec)
    return rec


def _kind_for(tier: str, symbol_kind: str) -> str:
    if tier == "a0_qk_constants":
        return "ui_variable" if symbol_kind == "variable" else "invariant"
    if tier == "a1_at_functions":
        return f"pure_{symbol_kind or 'function'}"
    if tier == "a2_mo_composites":
        return "engine_molecule"
    if tier == "a3_og_features":
        return "product_organism"
    if tier == "a4_sy_orchestration":
        return "ecosystem_system"
    return "component"


def propose_components(
    gaps: list[dict[str, Any]],
    root_id: str = "",
    *,
    source_rank: int = 0,
) -> list[ProposedComponent]:
    by_key: dict[str, ProposedComponent] = {}
    for gap in gaps:
        symbol = gap.get("source_symbol") or {}
        name = str(symbol.get("name") or "")
        if not name or name.startswith("_"):
            continue
        tier = str(gap.get("tier") or "a1_at_functions")
        categories = _normalize_categories(list(gap.get("product_categories") or []))
        dkey = _dedup_key(tier, name, categories)
        cid = str(gap.get("candidate_id") or (
            f"{_tier_prefix(tier)}.source.{_slug(root_id)}.{_slug(name)}"
        ))
        prop = ProposedComponent(
            id=cid,
            tier=tier,
            kind=_kind_for(tier, str(symbol.get("kind") or "")),
            name=name,
            source_symbol=dict(symbol),
            product_categories=categories,
            description=f"Draft candidate from {symbol.get('path', '')}:{symbol.get('line', 0)}.",
            dedup_key=dkey,
            source_rank=source_rank,
        )
        incumbent = by_key.get(dkey)
        if incumbent is None or _should_replace_incumbent(incumbent, prop):
            by_key[dkey] = prop
    return sorted(by_key.values(), key=_proposal_sort_key)


def _registry_ids(components: list[dict[str, Any]]) -> set[str]:
    out: set[str] = set()
    for c in components:
        cid = c.get("id")
        if cid:
            cid_str = str(cid)
            out.add(cid_str)
            out.add(fold_registry_token(cid_str))
    return out


def _match_blueprint(
    required_id: str, proposals: list[ProposedComponent], registry_ids: set[str]
) -> tuple[str, str | None]:
    if required_id in registry_ids or fold_registry_token(required_id) in registry_ids:
        return "registry", required_id
    nreq = fold_registry_token(required_id)
    for prop in proposals:
        if prop.id == required_id or fold_registry_token(prop.id) == nreq:
            prop.fulfills_blueprints.append(required_id)
            return "proposal", prop.id
    return "missing", None


def assess_blueprint_fulfillment(
    blueprints: list[dict[str, Any]],
    proposals: list[ProposedComponent],
    registry: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    registry_ids = _registry_ids(registry)
    out: list[dict[str, Any]] = []
    for bp in blueprints:
        required_ids: list[str] = []
        root = bp.get("root_component")
        if root:
            required_ids.append(str(root))
        for rid in bp.get("include_components") or []:
            required_ids.append(str(rid))
        for comp in bp.get("components") or []:
            if isinstance(comp, dict):
                cid = comp.get("id") or comp.get("name")
                if cid and str(cid) not in required_ids:
                    required_ids.append(str(cid))
            elif isinstance(comp, str) and comp not in required_ids:
                required_ids.append(comp)
        satisfied_registry: list[str] = []
        satisfied_proposal: list[dict[str, str]] = []
        missing: list[str] = []
        for rid in required_ids:
            status, matched = _match_blueprint(rid, proposals, registry_ids)
            if status == "registry":
                satisfied_registry.append(rid)
            elif status == "proposal":
                satisfied_proposal.append({"required": rid, "proposal": matched or ""})
            else:
                missing.append(rid)
        out.append({
            "blueprint_id": bp.get("id") or bp.get("blueprint_id"),
            "blueprint_name": bp.get("name") or bp.get("blueprint_name"),
            "visibility": bp.get("visibility"),
            "required_count": len(required_ids),
            "satisfied_by_registry": satisfied_registry,
            "satisfied_by_proposal": satisfied_proposal,
            "still_unfulfilled": missing,
            "fully_satisfied": len(missing) == 0,
        })
    return out


def _summarize_proposals(proposals: list[ProposedComponent]) -> dict[str, Any]:
    by_tier: dict[str, int] = {}
    by_category: dict[str, int] = {}
    blueprint_fillers = 0
    for p in proposals:
        by_tier[p.tier] = by_tier.get(p.tier, 0) + 1
        for cat in p.product_categories or ["COR"]:
            by_category[cat] = by_category.get(cat, 0) + 1
        if p.fulfills_blueprints:
            blueprint_fillers += 1
    return {
        "proposed_components": len(proposals),
        "blueprint_fillers": blueprint_fillers,
        "by_tier": by_tier,
        "by_category": by_category,
    }


def _dedupe_proposals_cross_root(
    all_proposals: list[ProposedComponent],
) -> tuple[dict[str, ProposedComponent], dict[str, list[dict[str, Any]]]]:
    """Merge proposals sharing ``dedup_key``; lower ``source_rank`` wins (0 = primary)."""
    dedup: dict[str, ProposedComponent] = {}
    sibling_sources: dict[str, list[dict[str, Any]]] = {}
    for prop in all_proposals:
        incumbent = dedup.get(prop.dedup_key)
        if incumbent is None:
            dedup[prop.dedup_key] = prop
            continue
        if _should_replace_incumbent(incumbent, prop):
            sibling_sources.setdefault(prop.dedup_key, []).append(incumbent.source_symbol)
            dedup[prop.dedup_key] = prop
            continue
        sibling_sources.setdefault(prop.dedup_key, []).append(prop.source_symbol)
    return dedup, sibling_sources


def build_gap_fill_plan(
    root_reports: list[dict[str, Any]],
    blueprints: list[dict[str, Any]] | None = None,
    registry: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    blueprints = blueprints or []
    registry = registry or []

    all_proposals: list[ProposedComponent] = []
    for rank, rr in enumerate(root_reports):
        root_id = str(rr.get("root_id") or Path(rr.get("source_root", "")).name)
        gaps = list(rr.get("gaps") or [])
        all_proposals.extend(propose_components(gaps, root_id=root_id, source_rank=rank))

    dedup, sibling_sources = _dedupe_proposals_cross_root(all_proposals)

    final_proposals = sorted(
        dedup.values(),
        key=lambda p: (p.source_rank, _proposal_sort_key(p)),
    )
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
