"""Tier a1 — assimilated function 'complete_function'

Assimilated from: rebuild/finish.py:178-229
"""

from __future__ import annotations


# --- assimilated symbol ---
def complete_function(
    fn: IncompleteFunction,
    *,
    base_url: str,
    api_key: str | None,
    agent_id: str | None,
    max_refinement_attempts: int = 3,
) -> tuple[str | None, list[dict[str, Any]]]:
    context_parts = [
        f"File: {fn.path.name}",
        f"Function: {fn.qualname}",
        f"Reason for completion: {fn.reason}",
        f"Signature:\n{fn.signature}",
    ]
    if fn.docstring:
        context_parts.append(f"Docstring:\n{fn.docstring}")
    context = "\n\n".join(context_parts)

    attempts: list[dict[str, Any]] = []
    feedback: str | None = None
    for attempt in range(1, max(1, max_refinement_attempts) + 1):
        candidate = _synthesize_via_nexus(
            component_id=fn.qualname,
            tier="a2_mo_composites",
            blueprint_id=f"finish:{fn.path.name}",
            context=context,
            base_url=base_url,
            api_key=api_key,
            agent_id=agent_id,
            language="python",
            adapter_id=None,
            feedback=feedback,
        )
        if candidate is None:
            attempts.append({"attempt": attempt, "status": "no_response"})
            break
        # Strip a leading markdown fence if the model ignored instructions.
        candidate = _strip_code_fence(candidate)
        # Accept only the *body* (not a redefinition of the function).
        body_only = _extract_body_only(candidate, fn.qualname.split(".")[-1])
        target = body_only or candidate
        probe = "def _probe():\n    pass\n\n" + (target if _looks_like_body(target) else candidate)
        ok, findings = _cie_gate(probe, "python")
        attempts.append({
            "attempt": attempt,
            "status": "passed" if ok else "cie_rejected",
            "findings": findings,
        })
        if ok:
            return target, attempts
        feedback = "; ".join(findings)
    return None, attempts

