"""Phase 1 multi-root ingest validation."""

from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.a3_og_features.phase1_ingest import run_phase1_ingest_multi


def test_root_ids_length_mismatch_raises(minimal_pkg_root: Path, tmp_path: Path) -> None:
    other = tmp_path / "other"
    other.mkdir()
    (other / "x.py").write_text("x = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="root_ids"):
        run_phase1_ingest_multi(
            [minimal_pkg_root, other],
            root_ids=["only_one"],
        )
