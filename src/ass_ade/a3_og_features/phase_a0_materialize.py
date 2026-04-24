"""Phase a0 — write tier-a0 stubs from a gap-fill plan (feature: I/O)."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.pipeline_meta import (
    A0_MATERIAL_SUBDIR,
    DEFAULT_A0_REBUILD_TAG_PREFIX,
    MINI_REBUILD_MATERIAL_SCHEMA,
)
from ass_ade.a1_at_functions.materialize_a0_plan import (
    certify_a0_layout,
    filter_a0_proposals,
    layout_a0_files,
)


def run_phase_a0_materialize(
    output_root: Path,
    gap_plan: dict[str, Any],
    *,
    rebuild_tag: str | None = None,
) -> dict[str, Any]:
    """Emit ``a0_qk_constants/*.py`` under ``output_root/<tag>/`` and return receipt."""
    output_root = output_root.resolve()
    proposals = filter_a0_proposals(gap_plan)
    files = layout_a0_files(proposals)
    certificate = certify_a0_layout(files, schema=MINI_REBUILD_MATERIAL_SCHEMA)
    tag = rebuild_tag or (
        f"{DEFAULT_A0_REBUILD_TAG_PREFIX}-"
        f"{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%S}Z"
    )
    target = output_root / tag / A0_MATERIAL_SUBDIR
    target.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    for rel, body in files.items():
        path = target / rel
        path.write_text(body, encoding="utf-8")
        written[rel] = path.as_posix()
    return {
        "phase": "a0_materialize",
        "material_schema": MINI_REBUILD_MATERIAL_SCHEMA,
        "rebuild_tag": tag,
        "target_root": target.as_posix(),
        "written": written,
        "summary": {"modules": len(files), "proposals": len(proposals)},
        "certificate": certificate,
        "gap_plan_digest": gap_plan.get("content_digest"),
    }
