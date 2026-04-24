"""Tier a1 — assimilated function 'load_coverage_manifest'

Assimilated from: rebuild/coverage_manifest.py:34-45
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal


# --- assimilated symbol ---
def load_coverage_manifest(root: Path, kind: CoverageKind) -> dict[str, Any] | None:
    """Load a generated coverage manifest when it exists and parses cleanly."""
    path = coverage_manifest_path(root, kind)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    expected_schema = TEST_COVERAGE_SCHEMA if kind == "test" else DOC_COVERAGE_SCHEMA
    if payload.get("schema") != expected_schema:
        return None
    return payload

