"""Directory names excluded when walking source trees (ingest / recon)."""

from __future__ import annotations

import fnmatch
import os

_BASE_EXCLUDED_DIRS = frozenset({
    ".git", ".venv", "venv", "node_modules", "engine_out", "target",
    "dist", "build", "rebuilds", "drafts", "__pycache__", ".pytest_cache",
    ".pytest_tmp", ".pytest_basetemp", "pytest_tmp", ".ruff_cache", ".next", ".turbo",
    ".import_linter_cache", "reports", "rebuild-outputs",
    ".ass-ade-pytest-basetemp",
    ".ass-ade", ".atomadic", ".claude", ".cursor", ".github", ".vscode",
})

_EXCLUDED_DIR_PATTERNS = frozenset({
    "*.egg-info",
    "*-backup-*",
    "ass-ade-v1-test*",
    ".ass-ade-pytest-basetemp*",
    ".claude-worktrees*",
})

_TIER_DIRS = frozenset({
    "a0_qk_constants", "a1_at_functions", "a2_mo_composites",
    "a3_og_features", "a4_sy_orchestration",
})

_SKIP_ENV = os.environ.get("ASS_ADE_SKIP_TIER_DIRS", "").lower() in ("1", "true", "yes")

EXCLUDED_DIRS: frozenset[str] = frozenset(
    _BASE_EXCLUDED_DIRS | (_TIER_DIRS if _SKIP_ENV else set())
)

EXCLUDED_DIR_PATTERNS: frozenset[str] = _EXCLUDED_DIR_PATTERNS

MAX_FILE_BYTES = 750_000

SOURCE_SUFFIXES = frozenset({".py"})


def is_excluded_dir_name(name: str) -> bool:
    """True when *name* should be skipped by repo walkers."""
    return name in EXCLUDED_DIRS or any(
        fnmatch.fnmatch(name, pattern) for pattern in EXCLUDED_DIR_PATTERNS
    )
