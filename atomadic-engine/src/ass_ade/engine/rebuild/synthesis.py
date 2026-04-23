"""Synthesis Engine — synthesize components for blueprint gaps.

When a blueprint requires a component that no source file provides, this
module synthesizes one via AAAA-Nexus inference with an *iterative
refinement loop* (CIE-gate failures are fed back into the next prompt,
up to ``max_refinement_attempts`` tries).

Production path ships **no stubs**: if the refinement loop exhausts
without a CIE-clean body, the component is recorded as rejected and —
when ``strict_no_stubs`` is True (default) — the overall synthesis call
raises :class:`SynthesisFailure`. A deterministic stub fallback remains
available behind ``allow_stub_fallback=True`` for tests and offline
demos, but is opt-in.

Every synthesized body goes through an AST + OWASP gate before being
added to the plan. Synthesized components carry ``status: synthesized``
so downstream tooling can distinguish them from extracted drafts.
"""

from __future__ import annotations

import ast
import datetime as dt
import importlib.resources as _pkg_resources
import os
import re
from typing import Any

from ass_ade.engine.rebuild.nexus_parse import (
    extract_json_array as _extract_json_array,
    extract_nexus_content as _extract_nexus_content,
    slugify as _slugify,
    strip_markdown_fences as _strip_markdown_fences,
)


class SynthesisFailure(RuntimeError):
    """Raised when strict no-stubs synthesis cannot produce a clean body."""


# Observable failure trail. Last Nexus error is surfaced in receipts so
# offline runs cannot silently pretend they were online.
_LAST_NEXUS_ERROR: str | None = None


def _record_nexus_error(msg: str) -> None:
    global _LAST_NEXUS_ERROR
    _LAST_NEXUS_ERROR = msg


def consume_last_nexus_error() -> str | None:
    """Return and clear the most recent Nexus failure. Used by orchestrators."""
    global _LAST_NEXUS_ERROR
    msg = _LAST_NEXUS_ERROR
    _LAST_NEXUS_ERROR = None
    return msg


_DRIVER_PROMPT_CACHE: str | None = None


def _load_driver_prompt() -> str:
    """Load the UEP-style synthesis driver prompt. Cached after first read."""
    global _DRIVER_PROMPT_CACHE
    if _DRIVER_PROMPT_CACHE is not None:
        return _DRIVER_PROMPT_CACHE
    try:
        ref = _pkg_resources.files("ass_ade.prompts").joinpath("uep_driver.md")
        _DRIVER_PROMPT_CACHE = ref.read_text(encoding="utf-8")
    except (FileNotFoundError, ModuleNotFoundError, AttributeError):
        _DRIVER_PROMPT_CACHE = ""
    return _DRIVER_PROMPT_CACHE

try:
    import httpx
except ImportError:  # pragma: no cover
    httpx = None  # type: ignore

DEFAULT_BASE_URL = os.environ.get("AAAA_NEXUS_BASE_URL", "https://atomadic.tech")

TIER_PREFIX: dict[str, str] = {
    "a0_qk_constants":      "qk",
    "a1_at_functions":      "at",
    "a2_mo_composites":     "mo",
    "a3_og_features":       "og",
    "a4_sy_orchestration":  "sy",
}

# OWASP patterns — hard-block any synthesized body that matches
_OWASP_CRITICAL: list[tuple[str, str]] = [
    (r"eval\s*\(", "A03_injection_eval"),
    (r"exec\s*\(", "A03_injection_exec"),
    (r"subprocess\.[a-z_]+\([^)]*shell\s*=\s*True", "A03_shell_injection"),
    (r"pickle\.loads?\s*\(", "A08_deserialization"),
    (r"__import__\s*\(", "A03_dynamic_import"),
]


def _tier_from_id(component_id: str) -> str:
    if not component_id:
        return "a1_at_functions"
    prefix = component_id.split(".", 1)[0]
    reverse = {v: k for k, v in TIER_PREFIX.items()}
    return reverse.get(prefix, "a1_at_functions")


def _infer_language(component_id: str) -> str:
    if "ui" in component_id.lower():
        return "typescript"
    if "kernel" in component_id.lower():
        return "rust"
    return "python"


def _fetch_current_adapter(base_url: str, language: str, api_key: str | None) -> str | None:
    if httpx is None:
        return None
    headers: dict[str, str] = {"User-Agent": "ass-ade-synthesis/1.0"}
    if api_key:
        headers["X-API-Key"] = api_key
    try:
        with httpx.Client(base_url=base_url, headers=headers, timeout=15.0) as c:
            r = c.get(f"/v1/lora/adapter/{language}")
            if r.status_code == 200:
                return r.json().get("adapter_id")
    except httpx.HTTPError as exc:
        _record_nexus_error(f"adapter lookup failed: {type(exc).__name__}: {exc}")
        return None
    return None


def _synthesize_via_nexus(
    component_id: str,
    tier: str,
    blueprint_id: str,
    context: str,
    *,
    base_url: str,
    api_key: str | None,
    agent_id: str | None,
    language: str,
    adapter_id: str | None,
    feedback: str | None = None,
) -> str | None:
    if httpx is None:
        return None
    driver = _load_driver_prompt()
    sections: list[str] = []
    if driver:
        sections.append(driver.strip())
    sections.append(
        f"Emit a minimal, production-grade {language} implementation of component "
        f"`{component_id}` for tier `{tier}` to fulfill blueprint `{blueprint_id}`. "
        f"Tier composition law: {tier} components compose only from the tier below. "
        f"Return ONLY the code body, no markdown fences, no commentary."
    )
    sections.append(f"Context:\n{context[:1500]}")
    if feedback:
        sections.append(
            "Previous attempt was rejected by the CIE gate. Fix ALL findings listed "
            f"below and return a clean body.\nFindings:\n{feedback}"
        )
    sections.append("Return the code body now.")
    prompt = "\n\n".join(sections)
    body: dict[str, Any] = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 900,
    }
    if adapter_id:
        body["lora"] = adapter_id
        body["language"] = language
    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "User-Agent": "ass-ade-synthesis/1.0",
    }
    if api_key:
        headers["X-API-Key"] = api_key
    if agent_id:
        headers["X-Agent-Id"] = agent_id
    try:
        with httpx.Client(base_url=base_url, headers=headers, timeout=45.0) as c:
            r = c.post("/v1/inference", json=body)
            if r.status_code != 200:
                _record_nexus_error(
                    f"http {r.status_code} from {base_url}/v1/inference: {r.text[:200]}"
                )
                return None
            data = r.json()
            text = _extract_nexus_content(data)
            if not text:
                _record_nexus_error(
                    f"empty content in Nexus response; keys={list(data.keys())[:8]}"
                )
            return text or None
    except httpx.HTTPError as exc:
        _record_nexus_error(f"httpx {type(exc).__name__}: {exc} (base_url={base_url})")
        return None


def _cie_gate(body: str, language: str) -> tuple[bool, list[str]]:
    """AST + OWASP pass over synthesized body. Returns (ok, findings)."""
    findings: list[str] = []
    if language == "python":
        try:
            ast.parse(body)
        except SyntaxError as exc:
            findings.append(f"SyntaxError:{exc.lineno}:{exc.msg}")
            return False, findings
    for pat, code in _OWASP_CRITICAL:
        if re.search(pat, body):
            findings.append(code)
    if findings and any(f.startswith("A0") for f in findings):
        return False, findings
    return True, findings


def _stub_body(component_id: str, tier: str, language: str) -> str:
    """Deterministic stub when no inference path is available."""
    if language == "python":
        safe_name = component_id.replace(".", "_")
        cls = "".join(part.title() for part in safe_name.split("_")) or "Component"
        return (
            f'"""Synthesized stub for {component_id} (tier {tier}).\n\n'
            f'Replace with real logic before shipping.\n'
            f'"""\n\n'
            f'from __future__ import annotations\n\n'
            f'from typing import Any\n\n\n'
            f'class {cls}:\n'
            f'    """Synthesized placeholder — implement before shipping."""\n\n'
            f'    def __init__(self, config: dict[str, Any] | None = None) -> None:\n'
            f'        self._config = config or {{}}\n\n'
            f'    def report(self) -> dict[str, Any]:\n'
            f'        return {{"component": "{component_id}", "tier": "{tier}", "status": "synthesized_stub"}}\n'
        )
    return f"// Synthesized stub for {component_id} (tier {tier}); replace before shipping.\n"


def _synthesized_component(
    component_id: str, body: str, language: str, blueprint_id: str, source: str
) -> dict[str, Any]:
    tier = _tier_from_id(component_id)
    # Normalize component_id to start with the correct tier prefix (Bug 3)
    expected_prefix = TIER_PREFIX.get(tier, "at") + "."
    if not component_id.startswith(expected_prefix):
        component_id = expected_prefix + component_id.replace(".", "_")
    name = component_id.split(".")[-1] or "component"
    last_seg = component_id.rsplit(".", 1)[-1]
    kind_map = {
        "a0_qk_constants":      "invariant",
        "a1_at_functions":      "pure_function",
        "a2_mo_composites":     "engine_molecule",
        "a3_og_features":       "product_organism",
        "a4_sy_orchestration":  "ecosystem_system",
    }
    return {
        "id": component_id,
        "tier": tier,
        "kind": kind_map.get(tier, "component"),
        "name": name,
        "description": f"Synthesized for blueprint {blueprint_id}.",
        "made_of": [],
        "product_categories": ["COR"],
        "fulfills_blueprints": [blueprint_id],
        "component_schema": "ASSADE-SPEC-003",
        "provides": [f"synthesized implementation of {component_id}"],
        "reuse_policy": "reference-only",
        "source_symbol": {
            "name": last_seg,
            "kind": "synthesized",
            "language": language,
            "path": f"synthesized://{component_id}",
            "line": 0,
        },
        "body": body,
        "body_truncated": False,
        "imports": [],
        "callers_of": [],
        "exceptions_raised": [],
        "status": "synthesized",
        "synthesis_source": source,
    }


def synthesize_missing_components(
    plan: dict[str, Any],
    *,
    base_url: str = DEFAULT_BASE_URL,
    api_key: str | None = None,
    agent_id: str | None = None,
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
