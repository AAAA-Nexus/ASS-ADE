"""Direct tests for Tarjan cycle detection (beyond phase-4 integration)."""

from __future__ import annotations

from ass_ade_v11.a1_at_functions.cycle_detector import break_cycles, detect_cycles


def test_detect_cycles_empty_plan_is_acyclic() -> None:
    r = detect_cycles({"proposed_components": []})
    assert r["acyclic"] is True
    assert r["cycle_count"] == 0


def test_detect_cycles_self_loop() -> None:
    r = detect_cycles({
        "proposed_components": [
            {"id": "a1.x", "tier": "a1_at_functions", "made_of": ["a1.x"]},
        ],
    })
    assert r["acyclic"] is False
    assert r["cycle_count"] >= 1


def test_break_cycles_removes_self_edge() -> None:
    plan = {
        "proposed_components": [
            {"id": "a1.x", "tier": "a1_at_functions", "made_of": ["a1.x", "a0.y"]},
        ],
    }
    rep = detect_cycles(plan)
    br = break_cycles(plan, rep)
    assert br["edges_removed"] >= 1
    assert plan["proposed_components"][0]["made_of"] == ["a0.y"]
