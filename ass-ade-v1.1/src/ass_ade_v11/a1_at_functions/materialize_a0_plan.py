"""Pure planning for a0-only materialization from a gap-fill plan (no I/O)."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from ass_ade_v11.a0_qk_constants.pipeline_meta import GENERATOR_STAMP


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "component"


def filter_a0_proposals(gap_plan: dict[str, Any]) -> list[dict[str, Any]]:
    """Return proposed components targeting ``a0_qk_constants`` only."""
    out: list[dict[str, Any]] = []
    for row in gap_plan.get("proposed_components") or []:
        if str(row.get("tier") or "") == "a0_qk_constants":
            out.append(dict(row))
    return sorted(out, key=lambda r: (r.get("dedup_key") or "", r.get("id") or ""))


def _stem_for_proposal(row: dict[str, Any]) -> str:
    name = str(row.get("name") or "symbol")
    dkey = str(row.get("dedup_key") or row.get("id") or "")
    h = hashlib.sha256(dkey.encode()).hexdigest()[:8]
    base = _slug(name)
    return f"gen_{base}_{h}"


def layout_a0_files(proposals: list[dict[str, Any]]) -> dict[str, str]:
    """Map relative paths (under ``a0_qk_constants/``) to file bodies."""
    files: dict[str, str] = {}
    for row in proposals:
        stem = _stem_for_proposal(row)
        rel = f"{stem}.py"
        sym = row.get("source_symbol") or {}
        path = str(sym.get("path") or "")
        line = sym.get("line") or 0
        kind = str(row.get("kind") or "")
        pid = str(row.get("id") or "")
        body = (
            '"""Generated a0 stub — do not edit by hand; regenerate from blueprint."""\n'
            f"# {GENERATOR_STAMP}\n\n"
            f"COMPONENT_ID = {pid!r}\n"
            f"SOURCE_PATH = {path!r}\n"
            f"SOURCE_LINE = {int(line)!r}\n"
            f"KIND = {kind!r}\n"
        )
        files[rel] = body
    return dict(sorted(files.items()))


def certify_a0_layout(
    files: dict[str, str],
    *,
    schema: str,
) -> dict[str, Any]:
    """Deterministic manifest + certificate over file contents (pure)."""
    manifest = {
        rel: hashlib.sha256(content.encode("utf-8")).hexdigest()
        for rel, content in sorted(files.items())
    }
    payload = json.dumps(
        {"schema": schema, "files": manifest},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    certificate_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return {
        "material_schema": schema,
        "manifest": manifest,
        "certificate_sha256": certificate_sha256,
        "module_count": len(files),
    }
