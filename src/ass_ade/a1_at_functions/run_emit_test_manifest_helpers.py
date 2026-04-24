"""Tier a1 — assimilated function 'run_emit_test_manifest'

Assimilated from: emit_test_manifest.py:11-19
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.test_synth_plan import plan_manifest_payload


# --- assimilated symbol ---
def run_emit_test_manifest(repo_root: Path) -> dict[str, Any]:
    """Write ``tests/generated_smoke/_qualnames.json`` from current sources."""
    repo_root = repo_root.resolve()
    out_dir = repo_root / "tests" / "generated_smoke"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "_qualnames.json"
    text = plan_manifest_payload(repo_root)
    path.write_text(text, encoding="utf-8")
    return {"written": path.as_posix(), "bytes": len(text.encode("utf-8"))}

