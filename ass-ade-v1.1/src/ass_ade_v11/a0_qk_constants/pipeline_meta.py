"""Pipeline metadata and interchange constants (a0 only — no logic)."""

from __future__ import annotations

# Distinct from gap_fill / ingestion schema: identifies a0-only materialization receipts.
MINI_REBUILD_MATERIAL_SCHEMA = "ASSADE-MAT-A0-V1"

# Default layout under output root: ``{output_root}/{rebuild_tag}/a0_qk_constants/``.
A0_MATERIAL_SUBDIR = "a0_qk_constants"

# Default tag prefix when caller does not supply ``rebuild_tag``.
DEFAULT_A0_REBUILD_TAG_PREFIX = "a0-mini"

# Provenance line embedded in generated stubs.
GENERATOR_STAMP = "ASS-ADE v1.1 — a0 materialize (MAP=TERRAIN)"
