"""Tier a1 — assimilated function 'emit_plan_blueprint'

Assimilated from: rebuild/schema_materializer.py:1295-1357
"""

from __future__ import annotations


# --- assimilated symbol ---
def emit_plan_blueprint(
    plan: dict[str, Any],
    *,
    out_dir: Path,
    rebuild_tag: str,
    registry_candidates: list[Atom] | None = None,
) -> dict[str, Any]:
    """Emit BLUEPRINT.plan.json — the *intended* state, BEFORE materialize.

    This is the guide. After materialize+forge we emit the realized
    BLUEPRINT.json and diff the two so the certificate can attest:
    "what was promised vs what was shipped".
    """
    target_root = out_dir / rebuild_tag
    target_root.mkdir(parents=True, exist_ok=True)
    plan_path = target_root / "BLUEPRINT.plan.json"
    proposed = plan.get("proposed_components") or []
    resolve_plan_canonical_names(
        proposed,
        registry_candidates=registry_candidates,
    )
    intended_atoms = sorted(
        [
            {
                "id": p.get("canonical_name")
                or canonical_name_for(
                    p,
                    fallback_tier=p.get("tier") or "a1_at_functions",
                    registry_candidates=registry_candidates,
                ),
                "tier": p.get("tier") or "",
                "name": p.get("name") or "",
                "kind": p.get("kind") or "function",
                "fulfills_blueprints": p.get("fulfills_blueprints") or [],
            }
            for p in proposed
            if p.get("canonical_name") or p.get("id")
        ],
        key=lambda r: (r["tier"], r["id"]),
    )
    # Dedupe by canonical id — strict naming means one atom per id, period.
    _seen_ids: set[str] = set()
    intended_atoms = [
        a for a in intended_atoms
        if a["id"] and not (a["id"] in _seen_ids or _seen_ids.add(a["id"]))
    ]
    body = {
        "blueprint_schema": "ASSADE-SPEC-BLUEPRINT-PLAN-1",
        "rebuild_tag": rebuild_tag,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_plan_digest": plan.get("content_digest"),
        "intended_count": len(intended_atoms),
        "intended_by_tier": _count_by_tier(intended_atoms),
        "atoms": intended_atoms,
    }
    blob = json.dumps(body, indent=2, sort_keys=True) + "\n"
    plan_path.write_text(blob, encoding="utf-8")
    return {
        "plan_blueprint_path": plan_path.as_posix(),
        "plan_blueprint_sha256": hashlib.sha256(blob.encode("utf-8")).hexdigest(),
        "intended_count": len(intended_atoms),
        "intended_atom_ids": {a["id"] for a in intended_atoms},
    }

