"""Tier a1 — assimilated function 'format_package_emit_episode_line'

Assimilated from: rebuild/autopoiesis_layout.py:35-59
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path

from ass_ade.engine.rebuild.autopoiesis_constants import (


# --- assimilated symbol ---
def format_package_emit_episode_line(
    *,
    utc_iso: str,
    vendored_ass_ade: bool,
    hatch_wheel_packages: list[str],
) -> str:
    """One JSON object per line for ``episodes.jsonl`` (no secrets, no raw env)."""
    payload = {
        "schema_version": EPISODE_SCHEMA_VERSION,
        "ts": utc_iso,
        "event": "package_emit",
        "vendored_ass_ade": vendored_ass_ade,
        "hatch_wheel_packages": list(hatch_wheel_packages),
        "evidence": [
            "src/ass_ade/engine/rebuild/package_emitter.py",
            "src/ass_ade/engine/rebuild/autopoiesis_layout.py",
        ],
        "rollback_hint": (
            "git checkout -- src/ass_ade/engine/rebuild/package_emitter.py "
            "src/ass_ade/engine/rebuild/autopoiesis_layout.py "
            "src/ass_ade/engine/rebuild/autopoiesis_constants.py; "
            "truncate or remove .ass-ade/memory/episodes.jsonl"
        ),
    }
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)

