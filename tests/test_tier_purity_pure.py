"""Direct tests for tier purity checker."""

from __future__ import annotations

from ass_ade.a1_at_functions.tier_purity import check_tier_purity


def test_a1_depending_on_a0_is_pure() -> None:
    plan = {
        "proposed_components": [
            {
                "id": "a1.demo.f",
                "tier": "a1_at_functions",
                "made_of": ["a0.demo.c"],
            },
        ],
    }
    r = check_tier_purity(plan)
    assert r["pure"] is True
    assert not r["violations"]


def test_a1_depending_on_a2_is_impure() -> None:
    plan = {
        "proposed_components": [
            {
                "id": "a1.demo.f",
                "tier": "a1_at_functions",
                "made_of": ["a2.demo.svc"],
            },
        ],
    }
    r = check_tier_purity(plan)
    assert r["pure"] is False
    assert any(v.get("bad_dep") == "a2.demo.svc" for v in r["violations"])
