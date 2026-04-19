# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_synthesize_missing_components.py:7
# Component id: at.source.a1_at_functions.synthesize_missing_components
from __future__ import annotations

__version__ = "0.1.0"

def synthesize_missing_components(
    plan: dict[str, Any],
    *,
    base_url: str = DEFAULT_BASE_URL,
    api_key: str | None = None,
    agent_id: str | None = None,
    allow_stub_fallback: bool = True,
    max_synthesize: int = 50,
) -> dict[str, Any]:
    """Synthesize components listed in blueprint ``still_unfulfilled``. Mutates ``plan``.

    Returns a receipt with ``synthesized_count``, ``lora_used``, ``stub_used``,
    ``rejected``, and ``synthesized_at``.
    """
    api_key = api_key or os.environ.get("AAAA_NEXUS_API_KEY")
    agent_id = agent_id or os.environ.get("AAAA_NEXUS_AGENT_ID")

    synthesized_ids: list[str] = []
    rejected: list[dict[str, Any]] = []
    stub_used = 0
    lora_used = 0

    for bp in plan.get("blueprint_fulfillment") or []:
        missing = list(bp.get("still_unfulfilled") or [])
        if not missing:
            continue
        for cid in missing:
            if len(synthesized_ids) >= max_synthesize:
                break
            tier = _tier_from_id(cid)
            language = _infer_language(cid)
            context = (
                f"Blueprint: {bp.get('blueprint_name') or bp.get('blueprint_id')}\n"
                f"Required component: {cid}\n"
                f"Target tier: {tier}"
            )
            adapter_id = _fetch_current_adapter(base_url, language, api_key) if api_key else None
            body = _synthesize_via_nexus(
                cid, tier, bp.get("blueprint_id") or "",
                context,
                base_url=base_url, api_key=api_key, agent_id=agent_id,
                language=language, adapter_id=adapter_id,
            )
            source = "lora"
            if body is None and allow_stub_fallback:
                body = _stub_body(cid, tier, language)
                source = "stub"
                stub_used += 1
            elif body is not None:
                lora_used += 1
            if body is None:
                rejected.append({"id": cid, "reason": "no_body_available"})
                continue
            ok, findings = _cie_gate(body, language)
            if not ok:
                rejected.append({"id": cid, "reason": "cie_gate", "findings": findings})
                if allow_stub_fallback and source == "lora":
                    body = _stub_body(cid, tier, language)
                    ok, findings = _cie_gate(body, language)
                    if ok:
                        source = "stub"
                        stub_used += 1
                    else:
                        continue
                else:
                    continue
            comp = _synthesized_component(cid, body, language, bp.get("blueprint_id") or "", source)
            plan.setdefault("proposed_components", []).append(comp)
            synthesized_ids.append(cid)
            bp.setdefault("satisfied_by_synthesis", []).append({
                "required": cid, "synthesis_source": source
            })
            if cid in bp.get("still_unfulfilled", []):
                bp["still_unfulfilled"].remove(cid)
            bp["fully_satisfied"] = len(bp.get("still_unfulfilled") or []) == 0

    receipt: dict[str, Any] = {
        "synthesized_count": len(synthesized_ids),
        "synthesized_ids": synthesized_ids,
        "lora_used": lora_used,
        "stub_used": stub_used,
        "rejected": rejected,
        "base_url": base_url,
        "synthesized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    plan.setdefault("summary", {})["synthesis"] = {
        "synthesized_count": receipt["synthesized_count"],
        "lora_used": lora_used,
        "stub_used": stub_used,
        "rejected_count": len(rejected),
    }
    return receipt
