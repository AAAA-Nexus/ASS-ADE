"""Contract: generated import manifest matches ``src/ass_ade_v11`` on disk."""

from __future__ import annotations

from pathlib import Path

from ass_ade_v11.a1_at_functions.test_synth_plan import manifest_drift


def test_qualnames_manifest_matches_sources() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    drift = manifest_drift(repo_root)
    assert drift["ok"], drift
