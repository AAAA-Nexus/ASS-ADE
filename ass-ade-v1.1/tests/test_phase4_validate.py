from __future__ import annotations

from ass_ade_v11.a3_og_features.phase4_validate import run_phase4_validate


def test_phase4_breaks_mutual_cycle() -> None:
    plan: dict = {
        "proposed_components": [
            {
                "id": "a1.source.x.a",
                "tier": "a1_at_functions",
                "name": "a",
                "made_of": ["a1.source.x.b"],
            },
            {
                "id": "a1.source.x.b",
                "tier": "a1_at_functions",
                "name": "b",
                "made_of": ["a1.source.x.a"],
            },
        ],
    }
    out = run_phase4_validate(plan, break_cycles_if_found=True, enforce_purity=False)
    assert out["cycles"]["acyclic"] is False
    assert out["cycles"]["break_receipt"]["edges_removed"] >= 1


def test_phase4_enforce_purity_strips_cross_a1_edge() -> None:
    plan: dict = {
        "proposed_components": [
            {
                "id": "a1.source.fixture.caller",
                "tier": "a1_at_functions",
                "name": "caller",
                "made_of": ["a1.source.fixture.helper"],
            },
            {
                "id": "a1.source.fixture.helper",
                "tier": "a1_at_functions",
                "name": "helper",
                "made_of": [],
            },
        ],
    }
    out = run_phase4_validate(plan, break_cycles_if_found=False, enforce_purity=True)
    assert "tier_purity" in out
    assert out["tier_purity"]["removed_edges"] >= 1
    caller = plan["proposed_components"][0]
    assert caller["made_of"] == []
