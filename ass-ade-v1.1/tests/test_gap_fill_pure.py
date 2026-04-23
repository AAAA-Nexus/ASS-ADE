"""Direct unit tests for ``gap_fill`` (beyond phase-2 integration)."""

from __future__ import annotations

from ass_ade_v11.a1_at_functions.gap_fill import (
    ProposedComponent,
    assess_blueprint_fulfillment,
    build_gap_fill_plan,
    propose_components,
)


def _gap(name: str, tier: str = "a1_at_functions", cid: str | None = None) -> dict:
    sym = {"name": name, "kind": "function", "path": f"src/{name}.py", "line": 1}
    row: dict = {
        "source_symbol": sym,
        "tier": tier,
        "product_categories": ["COR"],
        "status": "gap",
    }
    if cid:
        row["candidate_id"] = cid
    return row


def test_propose_components_skips_dunder_and_private() -> None:
    gaps = [
        _gap("__init__"),
        _gap("_private"),
        _gap("public_ok"),
    ]
    props = propose_components(gaps, root_id="pkg")
    assert len(props) == 1
    assert props[0].name == "public_ok"


def test_propose_components_dedupes_same_dedup_key() -> None:
    g1 = _gap("dup", cid="a1.source.a.dup")
    g2 = _gap("dup", cid="a1.source.b.dup")
    props = propose_components([g1, g2], root_id="pkg")
    assert len(props) == 1


def test_build_gap_fill_plan_stable_digest_and_proposals() -> None:
    report = {
        "root_id": "demo",
        "source_root": "/tmp/demo",
        "gaps": [_gap("alpha"), _gap("beta")],
    }
    plan = build_gap_fill_plan([report])
    assert plan["gap_fill_schema"].endswith("V11")
    assert len(plan["proposed_components"]) == 2
    assert plan["content_digest"]
    d2 = build_gap_fill_plan([report])["content_digest"]
    assert plan["content_digest"] == d2


def test_assess_blueprint_fully_satisfied_by_registry() -> None:
    proposals = [
        ProposedComponent(
            id="a1.prop.x",
            tier="a1_at_functions",
            kind="pure_function",
            name="x",
            source_symbol={"name": "x", "kind": "function", "path": "p.py", "line": 1},
            product_categories=["COR"],
        )
    ]
    registry = [{"id": "a0.existing.constant"}]
    blueprints = [{"id": "bp1", "root_component": "a0.existing.constant"}]
    rows = assess_blueprint_fulfillment(blueprints, proposals, registry)
    assert len(rows) == 1
    assert rows[0]["fully_satisfied"] is True
    assert rows[0]["still_unfulfilled"] == []


def test_assess_blueprint_missing_component() -> None:
    proposals: list = []
    registry: list = []
    blueprints = [{"id": "bp1", "root_component": "a1.nowhere.id"}]
    rows = assess_blueprint_fulfillment(blueprints, proposals, registry)
    assert rows[0]["fully_satisfied"] is False
    assert "a1.nowhere.id" in rows[0]["still_unfulfilled"]
