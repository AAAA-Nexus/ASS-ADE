"""Directory names excluded when walking source trees (ingest / recon)."""

from __future__ import annotations

import os

_BASE_EXCLUDED_DIRS = frozenset({
    ".git", ".venv", "venv", "node_modules", "engine_out", "target",
    "dist", "build", "rebuilds", "drafts", "__pycache__", ".pytest_cache",
    ".pytest_tmp", ".ruff_cache", ".next", ".turbo", "reports",
    ".ass-ade", ".atomadic", ".claude", ".cursor", ".github", ".vscode",
})

_TIER_DIRS = frozenset({
    "a0_qk_constants", "a1_at_functions", "a2_mo_composites",
    "a3_og_features", "a4_sy_orchestration",
})

_SKIP_ENV = os.environ.get("ASS_ADE_SKIP_TIER_DIRS", "").lower() in ("1", "true", "yes")

EXCLUDED_DIRS: frozenset[str] = frozenset(
    _BASE_EXCLUDED_DIRS | (_TIER_DIRS if _SKIP_ENV else set())
)

MAX_FILE_BYTES = 750_000

SOURCE_SUFFIXES = frozenset({".py"})
