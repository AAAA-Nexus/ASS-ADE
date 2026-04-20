"""Feature → blueprint proposer (Cap-C).

Takes a feature description plus an optional target codebase and asks
AAAA-Nexus to decompose it into tier-aligned components, then emits a
valid AAAA-SPEC-004 blueprint the user can build with ``ass-ade
blueprint build``.

This module is **deliberately light**: it produces a *blueprint*, not
code. Code is produced by the existing Cap-A pipeline.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ass_ade.engine.rebuild.synthesis import (
    DEFAULT_BASE_URL,
    _extract_nexus_content,
    _record_nexus_error,
)

try:
    import httpx  # type: ignore
except ImportError:
    httpx = None  # type: ignore


_VALID_TIERS = (
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
)
_TIER_PREFIX = {
    "a0_qk_constants": "qk",
    "a1_at_functions": "at",
    "a2_mo_composites": "mo",
    "a3_og_features": "og",
    "a4_sy_orchestration": "sy",
}


def _slug(text: str) -> str:
    # Split CamelCase first: `TokenBucket` -> `Token Bucket`.
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", text)
    out = re.sub(r"[^a-z0-9]+", "_", spaced.lower()).strip("_")
    return out or "component"


def _propose_via_nexus(
    description: str,
    *,
    target: Path | None,
    base_url: str,
    api_key: str | None,
    agent_id: str | None,
) -> list[dict[str, Any]] | None:
    if httpx is None:
        _record_nexus_error("feature.propose: httpx not installed")
        return None
    if api_key is None:
        _record_nexus_error(
            "feature.propose: AAAA_NEXUS_API_KEY not set (check .env load)"
        )
        return None
    context = ""
    if target and target.is_dir():
        top = sorted(p.name for p in target.iterdir() if not p.name.startswith("."))[:30]
        context = f"Target project top-level: {top}"
    prompt = (
        "You are a software architect. Decompose the feature below into a minimum set of "
        "tier-aligned components. Tiers: a0_qk_constants < a1_at_functions < a2_mo_composites "
        "< a3_og_features < a4_sy_orchestration. A component at tier N may only compose from "
        "tiers < N.\n\n"
        f"Feature description:\n{description}\n\n"
        f"{context}\n\n"
        "Return ONLY a JSON array of component objects with fields: "
        "`name` (snake_case), `tier` (one of the five tiers), `purpose` (one sentence), "
        "`signature` (a Python def signature). No markdown fences, no prose, no trailing text."
    )
    body = {"messages": [{"role": "user", "content": prompt}], "max_tokens": 900}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "ass-ade-feature/1.0",
        "X-API-Key": api_key,
    }
    if agent_id:
        headers["X-Agent-Id"] = agent_id
    try:
        with httpx.Client(base_url=base_url, headers=headers, timeout=45.0) as c:
            r = c.post("/v1/inference", json=body)
            if r.status_code != 200:
                _record_nexus_error(
                    f"feature.propose: http {r.status_code} from {base_url}: {r.text[:200]}"
                )
                return None
            data = r.json()
            text = _extract_nexus_content(data).strip()
            if not text:
                _record_nexus_error(
                    f"feature.propose: empty content; keys={list(data.keys())[:8]}"
                )
                return None
    except httpx.HTTPError as exc:
        _record_nexus_error(
            f"feature.propose: httpx {type(exc).__name__}: {exc} (base_url={base_url})"
        )
        return None
    return _parse_components(text)


def _parse_components(text: str) -> list[dict[str, Any]] | None:
    stripped = text.strip()
    if stripped.startswith("```"):
        nl = stripped.find("\n")
        stripped = stripped[nl + 1 :] if nl != -1 else stripped
        if stripped.endswith("```"):
            stripped = stripped[: -3]
    try:
        data = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, list):
        return None
    out: list[dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or "").strip()
        tier = str(item.get("tier") or "").strip()
        if not name or tier not in _VALID_TIERS:
            continue
        out.append({
            "name": _slug(name),
            "tier": tier,
            "purpose": str(item.get("purpose") or "").strip(),
            "signature": str(item.get("signature") or "").strip(),
        })
    return out or None


def _component_id(component: dict[str, Any]) -> str:
    prefix = _TIER_PREFIX[component["tier"]]
    return f"{prefix}_{_slug(component['name'])}"


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
