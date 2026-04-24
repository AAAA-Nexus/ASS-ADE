"""Direct unit tests for ``ingest`` helpers (beyond phase-1 integration)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.a1_at_functions.ingest import (
    Symbol,
    classify_symbol,
    classify_tier,
    extract_symbols,
    ingest_project,
    iter_source_files,
    product_categories,
)


def test_classify_tier_invariant_name_goes_a0() -> None:
    sym = Symbol("hold_invariant", "function", "python", "pkg/mod.py", 3)
    assert classify_tier(sym) == "a0_qk_constants"


def test_classify_tier_plain_function_defaults_a1() -> None:
    sym = Symbol("compute_total", "function", "python", "pkg/mod.py", 10)
    assert classify_tier(sym) == "a1_at_functions"


def test_classify_tier_class_defaults_a2() -> None:
    sym = Symbol("Widget", "class", "python", "pkg/widgets.py", 5)
    assert classify_tier(sym) == "a2_mo_composites"


def test_product_categories_pay_keyword() -> None:
    sym = Symbol("record_fee", "function", "python", "billing/core.py", 1)
    assert "PAY" in product_categories(sym)


def test_classify_symbol_registry_maps_status() -> None:
    reg = [{"id": "a1.registry.demo_unit", "name": "demo_unit"}]
    sym = Symbol("demo_unit", "function", "python", "t.py", 1)
    out = classify_symbol(sym, "root", reg)
    assert out["status"] == "mapped"
    assert out["candidate_id"] == "a1.registry.demo_unit"
    assert out["registry_match"] == "a1.registry.demo_unit"


def test_classify_symbol_gap_without_registry() -> None:
    sym = Symbol("lonely_fn", "function", "python", "t.py", 1)
    out = classify_symbol(sym, "myroot", [])
    assert out["status"] == "gap"
    assert "myroot" in out["candidate_id"]


def test_extract_symbols_syntax_error_returns_empty(tmp_path: Path) -> None:
    p = tmp_path / "broken.py"
    p.write_text("def (\n", encoding="utf-8")
    assert extract_symbols(p) == []


def test_iter_source_files_skips_excluded_package_dirs(tmp_path: Path) -> None:
    (tmp_path / "ok.py").write_text("def f():\n    pass\n", encoding="utf-8")
    bad_dir = tmp_path / "__pycache__"
    bad_dir.mkdir()
    (bad_dir / "hidden.py").write_text("def g(): pass\n", encoding="utf-8")
    files = list(iter_source_files(tmp_path))
    assert len(files) == 1
    assert files[0].name == "ok.py"


def test_ingest_project_emit_drafts_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="emit_drafts"):
        ingest_project(tmp_path, emit_drafts=True)


def test_ingest_project_progress_callback_error_is_swallowed(tmp_path: Path) -> None:
    (tmp_path / "m.py").write_text("def x():\n    return 1\n", encoding="utf-8")

    def boom(_i: int, _t: int) -> None:
        raise RuntimeError("nope")

    rep = ingest_project(tmp_path, root_id="t", progress_callback=boom)
    assert rep["summary"]["symbols"] >= 1
