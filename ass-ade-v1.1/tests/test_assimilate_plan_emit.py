from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade_v11.a1_at_functions.assimilate_plan_emit import (
    build_validate_assimilate_plan,
    default_assimilate_plan_schema_path,
)


def test_build_validate_assimilate_plan_minimal_ok(tmp_path: Path) -> None:
    sp = default_assimilate_plan_schema_path()
    if not sp.is_file():
        pytest.skip("plan schema missing")
    primary = tmp_path / "p"
    primary.mkdir()
    out = tmp_path / "o"
    out.mkdir()
    book = {
        "stopped_after": 2,
        "phase0": {"verdict": "READY_FOR_PHASE_1"},
        "phase1": {"namespace_conflicts": {"conflicts": [], "conflict_count": 0, "clean": True}},
        "phase2": {},
    }
    doc = build_validate_assimilate_plan(
        book=book,
        primary=primary,
        output_parent=out,
        extra_roots=[],
        stop_after_label="gapfill",
        policy=None,
    )
    assert doc["schema_version"] == "1"
    assert doc["ready_for_phase_1"] is True
    assert doc["book_stop_after"] == "gapfill"
