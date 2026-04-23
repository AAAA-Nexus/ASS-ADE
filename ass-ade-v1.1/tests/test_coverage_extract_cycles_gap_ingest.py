"""Coverage for body_extractor, cycle_detector, gap_fill, ingest."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from ass_ade_v11.a1_at_functions import body_extractor as be
from ass_ade_v11.a0_qk_constants.exclude_dirs import MAX_FILE_BYTES
from ass_ade_v11.a1_at_functions.body_extractor import (
    _extract_python_body,
    _extract_regex_body,
    derive_made_of_graph,
    enrich_components_with_bodies,
    extract_body,
)
from ass_ade_v11.a1_at_functions.cycle_detector import break_cycles, detect_cycles
from ass_ade_v11.a1_at_functions.gap_fill import (
    assess_blueprint_fulfillment,
    build_gap_fill_plan,
    propose_components,
)
from ass_ade_v11.a1_at_functions.ingest import (
    Symbol,
    classify_symbol,
    classify_tier,
    extract_symbols,
    ingest_project,
    product_categories,
)


def test_extract_python_syntax_error_returns_none() -> None:
    assert _extract_python_body("def foo(\n", "foo") is None


def test_extract_python_async_and_raise_call_and_attribute_call() -> None:
    src = """
import asyncio

async def callee():
    pass

class C:
    def meth(self):
        pass

async def target():
    callee()
    C().meth()
    raise ValueError("x")
"""
    body = _extract_python_body(src, "target")
    assert body is not None
    assert "async def target" in body.body
    assert "callee" in body.callers_of
    assert "meth" in body.callers_of
    assert "ValueError" in body.exceptions_raised


def test_extract_body_file_too_large_and_oserror(tmp_path: Path) -> None:
    p = tmp_path / "huge.py"
    p.write_bytes(b"#" * (be._MAX_FILE_BYTES + 1))
    assert extract_body(p, "x") is None

    p2 = tmp_path / "bad.py"
    p2.write_text("x=1\n", encoding="utf-8")

    def boom(*_a: object, **_k: object) -> str:
        raise OSError("read")

    with patch.object(Path, "read_text", boom):
        assert extract_body(p2, "n") is None


def test_extract_regex_rust_and_js_like(tmp_path: Path) -> None:
    rust = tmp_path / "x.rs"
    rust.write_text(
        "// Extracted from elsewhere\n// Component id: z\n\nuse std::io;\nfn target() { let _ = 1; }\n",
        encoding="utf-8",
    )
    b = extract_body(rust, "target", language="rust")
    assert b is not None
    assert "std::io" in b.imports

    js = tmp_path / "x.ts"
    js.write_text(
        "import { x } from 'mod';\nconst target = () => x();\n",
        encoding="utf-8",
    )
    b2 = extract_body(js, "target", language="typescript")
    assert b2 is not None
    assert "mod" in b2.imports


def test_enrich_plan_truncates_and_skips(tmp_path: Path) -> None:
    py = tmp_path / "m.py"
    py.write_text("def hello():\n    return 42\n", encoding="utf-8")
    plan: dict = {
        "proposed_components": [
            {"name": "hello", "source_symbol": {"path": str(py), "name": "hello"}},
            {"name": "nope", "source_symbol": {"path": "", "name": "nope"}},
        ],
    }
    enrich_components_with_bodies(plan, max_body_chars=5)
    prop = plan["proposed_components"][0]
    assert prop["body_truncated"] is True
    assert len(prop["body"]) == 5


def test_extract_python_no_symbol_and_raise_call() -> None:
    assert _extract_python_body("x = 1\n", "missing") is None
    src = "def target():\n    raise ValueError()\n"
    body = _extract_python_body(src, "target")
    assert body is not None
    assert "ValueError" in body.exceptions_raised
    src_name = "def target():\n    raise RuntimeError\n"
    body_n = _extract_python_body(src_name, "target")
    assert body_n is not None
    assert "RuntimeError" in body_n.exceptions_raised


def test_extract_regex_no_match() -> None:
    assert _extract_regex_body("no symbol here", "nope", "rust") is None


def test_enrich_skips_when_extract_fails() -> None:
    plan: dict = {
        "proposed_components": [
            {"name": "n", "source_symbol": {"path": "/nonexistent/nope.py", "name": "n"}},
        ],
    }
    enrich_components_with_bodies(plan)
    assert "body" not in plan["proposed_components"][0]


def test_derive_made_of_graph_links() -> None:
    plan = {
        "proposed_components": [
            {"id": "a1.a", "name": "Main", "callers_of": ["helper"], "made_of": []},
            {"id": "a1.b", "name": "helper", "callers_of": [], "made_of": []},
        ],
    }
    derive_made_of_graph(plan)
    assert "a1.b" in plan["proposed_components"][0]["made_of"]


def test_detect_cycles_skips_empty_id_and_self_loop_and_tarjan() -> None:
    plan = {
        "proposed_components": [
            {"id": "", "made_of": ["a1.x"]},
            {"id": "a1.self", "made_of": ["a1.self", "a1.b"]},
            {"id": "a1.b", "made_of": ["a1.self"]},
        ],
    }
    rep = detect_cycles(plan)
    assert rep["acyclic"] is False
    assert rep["cycle_count"] >= 1


def test_break_cycles_empty_and_self_and_multi(tmp_path: Path) -> None:
    assert break_cycles({}, {"cycles": []}) == {"edges_removed": 0, "nodes_affected": []}

    plan = {
        "proposed_components": [
            {"id": "a1.a", "made_of": ["a1.a", "a1.b"]},
            {"id": "a1.b", "made_of": ["a1.a"]},
        ],
    }
    rep = detect_cycles(plan)
    br = break_cycles(plan, rep)
    assert br["edges_removed"] >= 1

    plan2 = {
        "proposed_components": [
            {"id": "x", "made_of": []},
        ],
    }
    br2 = break_cycles(plan2, {"cycles": [[], ["x"]]})
    assert br2["edges_removed"] == 0

    plan3 = {
        "proposed_components": [
            {"id": "m2.a", "made_of": ["m2.b"]},
            {"id": "m2.b", "made_of": ["m2.a"]},
        ],
    }
    rep3 = detect_cycles(plan3)
    br3 = break_cycles(plan3, rep3)
    assert br3["edges_removed"] >= 1

    br4 = break_cycles(
        {"proposed_components": [{"id": "solo", "made_of": []}]},
        {"cycles": [["solo", "ghost.missing"]]},
    )
    assert br4["edges_removed"] >= 0


def test_gap_fill_kind_branches_and_default_component() -> None:
    from ass_ade_v11.a1_at_functions import gap_fill as gf

    assert gf._kind_for("a0_qk_constants", "variable") == "ui_variable"
    assert gf._kind_for("a0_qk_constants", "class") == "invariant"
    assert gf._kind_for("a1_at_functions", "") == "pure_function"
    assert gf._kind_for("a2_mo_composites", "function") == "engine_molecule"
    assert gf._kind_for("a3_og_features", "function") == "product_organism"
    assert gf._kind_for("a4_sy_orchestration", "function") == "ecosystem_system"
    assert gf._kind_for("unknown_tier_xyz", "function") == "component"
    assert gf._tier_prefix("unknown_tier_xyz") == "a1"


def test_propose_components_skips_private_and_uses_candidate_id() -> None:
    gaps = [
        {
            "tier": "a1_at_functions",
            "source_symbol": {"name": "_hidden", "path": "p", "line": 1, "kind": "function"},
        },
        {
            "tier": "a1_at_functions",
            "candidate_id": "a1.custom.id",
            "source_symbol": {"name": "Visible", "path": "p", "line": 2, "kind": "function"},
        },
    ]
    props = propose_components(gaps, root_id="root")
    assert len(props) == 1
    assert props[0].id == "a1.custom.id"


def test_build_gap_fill_dedup_sibling_branches_and_blueprint_assess() -> None:
    sym_a = {"name": "Dup", "path": "a.py", "line": 1, "kind": "function"}
    sym_b = {"name": "Dup", "path": "b.py", "line": 2, "kind": "function"}
    rr1 = {
        "root_id": "r1",
        "gaps": [{"tier": "a1_at_functions", "source_symbol": sym_a, "product_categories": ["COR"]}],
    }
    rr2 = {
        "root_id": "r2",
        "gaps": [{"tier": "a1_at_functions", "source_symbol": sym_b, "product_categories": ["COR"]}],
    }
    registry = [{"id": "a1.registry.k", "name": "keeper"}]
    blueprints = [
        {
            "id": "bp1",
            "name": "B",
            "root_component": "a1.registry.k",
            "include_components": ["missing.one"],
            "components": [{"id": "a1.source.r1.dup"}, "stray"],
        },
    ]
    plan = build_gap_fill_plan([rr1, rr2], blueprints=blueprints, registry=registry)
    assert plan["summary"]["deduped_dropped"] >= 1

    rr_big = {
        "root_id": "zzz",
        "gaps": [{"tier": "a1_at_functions", "source_symbol": sym_a, "product_categories": ["COR"]}],
    }
    rr_small = {
        "root_id": "aaa",
        "gaps": [{"tier": "a1_at_functions", "source_symbol": sym_b, "product_categories": ["COR"]}],
    }
    plan2 = build_gap_fill_plan([rr_big, rr_small], blueprints=[], registry=[])
    assert plan2["summary"]["deduped_dropped"] >= 1
    fulfill = plan["blueprint_fulfillment"][0]
    assert fulfill["satisfied_by_registry"]
    assert fulfill["still_unfulfilled"]

    from ass_ade_v11.a1_at_functions.gap_fill import ProposedComponent, _match_blueprint

    pobj = ProposedComponent(
        id="a1.source.r1.dup",
        tier="a1_at_functions",
        kind="pure_function",
        name="Dup",
        source_symbol=dict(sym_a),
        product_categories=["COR"],
    )
    st, mid = _match_blueprint("a1.source.r1.dup", [pobj], {"x"})
    assert st == "proposal"
    assert mid == "a1.source.r1.dup"


def test_assess_blueprint_components_variants() -> None:
    from ass_ade_v11.a1_at_functions.gap_fill import ProposedComponent

    bp = {
        "blueprint_id": "b",
        "root_component": "r",
        "components": [{"id": "r", "name": "n"}, "extra"],
    }
    prop = ProposedComponent(
        id="a1.x",
        tier="a1_at_functions",
        kind="k",
        name="n",
        source_symbol={},
        product_categories=["COR"],
    )
    out = assess_blueprint_fulfillment([bp], [prop], [])
    assert out[0]["required_count"] >= 2


def test_ingest_classify_and_product_categories_and_extract(tmp_path: Path) -> None:
    assert classify_tier(Symbol("x", "class", "python", "engine_service.py", 1)) == "a2_mo_composites"
    assert classify_tier(Symbol("x", "function", "python", "registry_gateway.py", 1)) == "a3_og_features"
    assert classify_tier(Symbol("main", "function", "python", "router_runtime.py", 1)) == "a4_sy_orchestration"
    assert classify_tier(Symbol("z", "function", "python", "plain.py", 1)) == "a1_at_functions"
    assert classify_tier(Symbol("C", "class", "python", "plain2.py", 1)) == "a2_mo_composites"
    assert classify_tier(Symbol("foo", "other", "python", "plain2.py", 1)) == "a1_at_functions"

    assert "IDT" in product_categories(Symbol("u", "function", "python", "identity_ucan.py", 1))
    assert "DCM" in product_categories(Symbol("u", "function", "python", "theorem_rag.py", 1))
    assert "SEC" in product_categories(Symbol("u", "function", "python", "security_pqc.py", 1))

    bad = tmp_path / "bad.py"
    bad.write_text("def a(\n", encoding="utf-8")
    assert extract_symbols(bad) == []

    huge = tmp_path / "huge.py"
    huge.write_bytes(b"pass\n" * (MAX_FILE_BYTES // 5 + 1000))
    assert extract_symbols(huge) == []

    txt = tmp_path / "x.txt"
    txt.write_text("hello", encoding="utf-8")
    assert extract_symbols(txt) == []

    with patch.object(Path, "read_text", side_effect=OSError("no")):
        ok = tmp_path / "ok.py"
        ok.write_text("x=1\n", encoding="utf-8")
        assert extract_symbols(ok) == []


def test_ingest_emit_drafts_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="emit_drafts"):
        ingest_project(tmp_path, emit_drafts=True)


def test_ingest_progress_callback_swallows_exception(tmp_path: Path) -> None:
    (tmp_path / "m.py").write_text("def f():\n    pass\n", encoding="utf-8")

    def cb(_i: int, _t: int) -> None:
        raise RuntimeError("boom")

    rep = ingest_project(tmp_path, progress_callback=cb)
    assert rep["summary"]["files_scanned"] >= 1


def test_classify_symbol_registry_match_and_substring_keys() -> None:
    sym = Symbol("MyAtomButton", "function", "python", "p.py", 1)
    registry = [{"id": "a1.reg.longid", "name": "MyAtomButton"}]
    row = classify_symbol(sym, "root", registry)
    assert row["status"] == "mapped"

    sym2 = Symbol("atom", "function", "python", "plain.py", 1)
    registry2 = [{"id": "a1.x", "name": "MyAtomButton"}]
    row2 = classify_symbol(sym2, "root", registry2)
    assert row2["registry_match"] == "a1.x"


def test_match_registry_impl_stem(tmp_path: Path) -> None:
    from ass_ade_v11.a1_at_functions.registry_fingerprint import match_registry_row

    impl = tmp_path / "foo_bar.py"
    impl.write_text("x=1\n", encoding="utf-8")
    reg = [{"id": "a1.z", "name": "other", "_implementation": str(impl)}]
    assert match_registry_row("foobar", reg) == "a1.z"
    assert match_registry_row("foo_bar", reg) == "a1.z"


def test_stable_registry_row_payload_optional_fields() -> None:
    from ass_ade_v11.a1_at_functions.registry_fingerprint import stable_registry_row_payload

    p = stable_registry_row_payload({"id": "a", "name": "b", "tier": "t", "kind": "k"})
    assert '"tier"' in p and '"kind"' in p

