"""Tier a1 — assimilated function 'synthesize_missing_components'

Assimilated from: rebuild/synthesis.py:424-582
"""

from __future__ import annotations


# --- assimilated symbol ---
def synthesize_missing_components(
    plan: dict[str, Any],
    *,
    base_url: str = DEFAULT_BASE_URL,
    api_key: str | None = None,
    agent_id: str | None = None,
    registry_candidates: list[Atom] | None = None,
    allow_stub_fallback: bool = False,
    strict_no_stubs: bool = True,
    max_synthesize: int = 50,
    max_refinement_attempts: int = 3,
) -> dict[str, Any]:
    """Synthesize components listed in blueprint ``still_unfulfilled``. Mutates ``plan``.

    Production path (``strict_no_stubs=True``, the default) runs an iterative
    refinement loop against AAAA-Nexus: on each CIE-gate failure the findings
    are fed back into the next prompt, up to ``max_refinement_attempts`` tries.
    If the loop exhausts, a :class:`SynthesisFailure` is raised listing the
    components that could not be produced cleanly.

    Legacy behaviour (one-shot + deterministic stub) is still available by
    setting ``allow_stub_fallback=True`` and ``strict_no_stubs=False`` — this
    is intended for tests and offline demos.

    Returns a receipt with ``synthesized_count``, ``lora_used``, ``stub_used``,
    ``rejected``, ``refinement_trace``, and ``synthesized_at``.
    """
    api_key = api_key or os.environ.get("AAAA_NEXUS_API_KEY")
    agent_id = agent_id or os.environ.get("AAAA_NEXUS_AGENT_ID")

    synthesized_ids: list[str] = []
    rejected: list[dict[str, Any]] = []
    refinement_trace: list[dict[str, Any]] = []
    stub_used = 0
    lora_used = 0

    for bp in plan.get("blueprint_fulfillment") or []:
        missing = list(bp.get("still_unfulfilled") or [])
        missing_metadata = bp.get("still_unfulfilled_metadata") or {}
        if not missing:
            continue
        for raw_required in missing:
            if len(synthesized_ids) >= max_synthesize:
                break
            requirement = dict(missing_metadata.get(raw_required) or {})
            requirement.setdefault("required", raw_required)
            cid = _resolve_requirement_component_id(
                requirement,
                registry_candidates=registry_candidates,
            )
            tier = _requirement_tier(requirement, cid)
            language = _requirement_language(requirement, cid)
            context = _build_requirement_context(
                bp,
                requirement,
                raw_required,
                cid,
                tier,
            )
            adapter_id = _fetch_current_adapter(base_url, language, api_key) if api_key else None

            body: str | None = None
            source = "lora"
            attempt_findings: list[str] = []
            attempts_log: list[dict[str, Any]] = []
            feedback: str | None = None
            for attempt in range(1, max(1, max_refinement_attempts) + 1):
                candidate = _synthesize_via_nexus(
                    cid, tier, bp.get("blueprint_id") or "",
                    context,
                    base_url=base_url, api_key=api_key, agent_id=agent_id,
                    language=language, adapter_id=adapter_id,
                    feedback=feedback,
                )
                if candidate is None:
                    attempts_log.append({"attempt": attempt, "status": "no_response"})
                    break
                ok, findings = _cie_gate(candidate, language)
                attempts_log.append({
                    "attempt": attempt,
                    "status": "passed" if ok else "cie_rejected",
                    "findings": findings,
                })
                if ok:
                    body = candidate
                    break
                attempt_findings = findings
                feedback = "; ".join(findings)

            if attempts_log:
                refinement_trace.append({
                    "id": cid,
                    "tier": tier,
                    "language": language,
                    "attempts": attempts_log,
                })

            if body is None and allow_stub_fallback:
                candidate = _stub_body(cid, tier, language)
                ok, findings = _cie_gate(candidate, language)
                if ok:
                    body = candidate
                    source = "stub"
                    stub_used += 1

            if body is None:
                rejected.append({
                    "id": cid,
                    "reason": "refinement_exhausted",
                    "findings": attempt_findings,
                    "attempts": len(attempts_log),
                })
                continue

            if source == "lora":
                lora_used += 1

            comp = _synthesized_component(cid, body, language, bp.get("blueprint_id") or "", source)
            plan.setdefault("proposed_components", []).append(comp)
            synthesized_ids.append(cid)
            bp.setdefault("satisfied_by_synthesis", []).append({
                "required": raw_required,
                "canonical_name": cid,
                "synthesis_source": source,
            })
            if raw_required in bp.get("still_unfulfilled", []):
                bp["still_unfulfilled"].remove(raw_required)
            elif cid in bp.get("still_unfulfilled", []):
                bp["still_unfulfilled"].remove(cid)
            bp["fully_satisfied"] = len(bp.get("still_unfulfilled") or []) == 0

    receipt: dict[str, Any] = {
        "synthesized_count": len(synthesized_ids),
        "synthesized_ids": synthesized_ids,
        "lora_used": lora_used,
        "stub_used": stub_used,
        "rejected": rejected,
        "refinement_trace": refinement_trace,
        "base_url": base_url,
        "last_nexus_error": consume_last_nexus_error(),
        "synthesized_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    plan.setdefault("summary", {})["synthesis"] = {
        "synthesized_count": receipt["synthesized_count"],
        "lora_used": lora_used,
        "stub_used": stub_used,
        "rejected_count": len(rejected),
        "refinement_attempts_total": sum(len(t["attempts"]) for t in refinement_trace),
    }

    if strict_no_stubs and rejected:
        ids = ", ".join(r["id"] for r in rejected)
        raise SynthesisFailure(
            f"Synthesis failed for {len(rejected)} component(s) after "
            f"{max_refinement_attempts} refinement attempt(s): {ids}. "
            f"Set strict_no_stubs=False with allow_stub_fallback=True to accept stubs."
        )

    return receipt

