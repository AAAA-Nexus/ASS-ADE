from __future__ import annotations

from pathlib import Path

from ass_ade.a0_qk_constants.schemas import REGISTRY_SNAPSHOT_SCHEMA
from ass_ade.a1_at_functions.ingest import ingest_project
from ass_ade.a1_at_functions.registry_fingerprint import (
    fingerprint_gap_proposal,
    fingerprint_registry_row,
    fold_registry_token,
    match_registry_row,
    registry_snapshot_ledger,
)


def test_fold_registry_token_matches_legacy_normalize() -> None:
    assert fold_registry_token("Ab.C-d/12") == "abcd12"


def test_match_registry_row_by_name_and_id() -> None:
    reg = [
        {"id": "a1.registry.Alpha", "name": "Alpha"},
        {"id": "a2.impl.Beta", "name": "Other", "_implementation": "src/foo_beta.py"},
    ]
    assert match_registry_row("Alpha", reg) == "a1.registry.Alpha"
    assert match_registry_row("Beta", reg) == "a2.impl.Beta"


def test_registry_snapshot_order_invariant() -> None:
    rows_a = [
        {"id": "z.last", "name": "Z"},
        {"id": "a.first", "name": "A"},
    ]
    rows_b = list(reversed(rows_a))
    assert (
        registry_snapshot_ledger(rows_a)["registry_snapshot_sha256"]
        == registry_snapshot_ledger(rows_b)["registry_snapshot_sha256"]
    )


def test_registry_snapshot_golden() -> None:
    rows = [
        {"id": "a1.demo.Foo", "name": "Foo"},
        {"id": "a0.core.bar", "name": "bar"},
    ]
    snap = registry_snapshot_ledger(rows)
    assert snap["registry_snapshot_schema"] == REGISTRY_SNAPSHOT_SCHEMA
    assert snap["registry_snapshot_sha256"] == (
        "63a5b580eec4553cd03c3801403da4da7d5efffe202bc6dd666bf5676d4ebe53"
    )


def test_fingerprint_registry_row_stable() -> None:
    row = {"id": "x.y.Z", "name": "Z"}
    a = fingerprint_registry_row(row)
    b = fingerprint_registry_row(dict(row))
    assert a == b
    assert len(a) == 64


def test_fingerprint_gap_proposal_ignores_extra_keys() -> None:
    base = {
        "id": "p1",
        "tier": "a1_at_functions",
        "kind": "pure_function",
        "name": "n",
        "description": "",
        "made_of": [],
        "product_categories": ["COR"],
        "fulfills_blueprints": [],
        "source_symbol": {},
        "dedup_key": "k",
        "sibling_source_count": 0,
    }
    a = fingerprint_gap_proposal(base)
    noisy = {**base, "noise": 99, "fingerprint_sha256": "deadbeef"}
    b = fingerprint_gap_proposal(noisy)
    assert a == b


def test_ingest_attaches_registry_snapshot(minimal_pkg_root: Path) -> None:
    registry = [{"id": "a1.stub.pure_helper", "name": "pure_helper"}]
    rep = ingest_project(minimal_pkg_root, root_id="fixture", registry=registry)
    assert rep["registry_snapshot"] is not None
    assert rep["registry_snapshot"]["component_count"] == 1
    mapped = [c for c in rep["candidate_components"] if c["status"] == "mapped"]
    assert any(c["source_symbol"]["name"] == "pure_helper" for c in mapped)
