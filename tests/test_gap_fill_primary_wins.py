"""Primary root (source_rank 0) wins over secondary on same dedup_key."""

from __future__ import annotations

from ass_ade.a1_at_functions.gap_fill import build_gap_fill_plan


def test_build_gap_fill_primary_beats_secondary_on_same_symbol() -> None:
    sym_pri = {"name": "SharedFn", "kind": "function", "path": "primary/a.py", "line": 1}
    sym_sec = {"name": "SharedFn", "kind": "function", "path": "secondary/b.py", "line": 2}
    pri = {
        "root_id": "ass_ade",
        "source_root": "/pri",
        "gaps": [{"source_symbol": sym_pri, "tier": "a1_at_functions", "product_categories": ["COR"]}],
    }
    sec = {
        "root_id": "ass_ade_legacy",
        "source_root": "/sec",
        "gaps": [{"source_symbol": sym_sec, "tier": "a1_at_functions", "product_categories": ["COR"]}],
    }
    plan = build_gap_fill_plan([pri, sec])
    assert len(plan["proposed_components"]) == 1
    row = plan["proposed_components"][0]
    assert row["source_symbol"]["path"] == "primary/a.py"
    assert row.get("source_rank") == 0


def test_build_gap_fill_secondary_only_when_unique() -> None:
    sym_sec = {"name": "OnlyInSecondary", "kind": "function", "path": "s/x.py", "line": 1}
    pri = {"root_id": "p", "source_root": "/p", "gaps": []}
    sec = {
        "root_id": "s",
        "source_root": "/s",
        "gaps": [{"source_symbol": sym_sec, "tier": "a1_at_functions", "product_categories": ["COR"]}],
    }
    plan = build_gap_fill_plan([pri, sec])
    names = {c["name"] for c in plan["proposed_components"]}
    assert "OnlyInSecondary" in names
