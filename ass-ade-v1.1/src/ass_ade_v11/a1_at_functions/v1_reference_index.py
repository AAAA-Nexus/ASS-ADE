"""Index ass-ade-v1* reference trees for MAP=TERRAIN receipts (pure path probes)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ass_ade_v11.a0_qk_constants.reference_roots import (
    ASS_ADE_V1_LINEAGE_GLOB,
    ASS_ADE_V1_REFERENCE_ROOT_ENV,
    DOCUMENTED_ASS_ADE_V1_REFERENCE_ROOT,
    REFERENCE_BLUEPRINT_BASENAME,
    REFERENCE_CERTIFICATE_BASENAME,
    REFERENCE_MANIFEST_BASENAME,
    REFERENCE_PROVENANCE_BASENAME,
)


def resolve_ass_ade_v1_reference_root() -> Path | None:
    """Return a directory path if configured and present, else ``None``."""
    raw = os.environ.get(ASS_ADE_V1_REFERENCE_ROOT_ENV, DOCUMENTED_ASS_ADE_V1_REFERENCE_ROOT)
    root = Path(raw)
    try:
        if root.is_dir():
            return root.resolve()
    except OSError:
        return None
    return None


def index_reference_root(root: Path) -> dict[str, Any]:
    """Probe expected ass-ade-v1 artifacts under ``root`` (no parsing)."""
    r = root.resolve()
    return {
        "lineage_glob": ASS_ADE_V1_LINEAGE_GLOB,
        "root": r.as_posix(),
        "manifest_json": (r / REFERENCE_MANIFEST_BASENAME).is_file(),
        "certificate_json": (r / REFERENCE_CERTIFICATE_BASENAME).is_file(),
        "blueprint_json": (r / REFERENCE_BLUEPRINT_BASENAME).is_file(),
        "provenance_json": (r / REFERENCE_PROVENANCE_BASENAME).is_file(),
    }


def attach_v1_reference_index(book: dict[str, Any]) -> dict[str, Any]:
    """Mutate and return ``book`` with ``reference_ass_ade_v1`` (MAP=TERRAIN)."""
    root = resolve_ass_ade_v1_reference_root()
    if root is None:
        book["reference_ass_ade_v1"] = {
            "indexed": False,
            "lineage_glob": ASS_ADE_V1_LINEAGE_GLOB,
            "env": ASS_ADE_V1_REFERENCE_ROOT_ENV,
            "documented_default": DOCUMENTED_ASS_ADE_V1_REFERENCE_ROOT,
        }
        return book
    book["reference_ass_ade_v1"] = {"indexed": True, **index_reference_root(root)}
    return book
