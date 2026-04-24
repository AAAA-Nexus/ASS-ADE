"""Tests for Phase E — gap-fill pipeline + hot-patch runtime + endpoints."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from ass_ade.a2_mo_composites.block_registry import BlockRegistry
from ass_ade.a3_og_features.composition_engine import (
    CompositionEdge,
    CompositionNode,
    CompositionPlan,
    Gap,
)
from ass_ade.a3_og_features.gap_fill_pipeline import (
    GapFillPipeline,
    _stub_body,
    _validate_synthesized,
)
from ass_ade.a3_og_features.hot_patch_runtime import (
    _BLOCKLIST,
    hot_patch,
    module_for_path,
    reload_module,
)


# ── Fixture ────────────────────────────────────────────────────────────────

def _make_pkg(root: Path) -> Path:
    pkg = root / "demo_pkg"
    for tier in (
        "a0_qk_constants", "a1_at_functions", "a2_mo_composites",
        "a3_og_features", "a4_sy_orchestration",
    ):
        (pkg / tier).mkdir(parents=True)
        (pkg / tier / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "a1_at_functions" / "ping.py").write_text(
        '"""Ping."""\n\n'
        'def ping(results: dict):\n'
        '    """Say pong."""\n'
        '    return "pong"\n',
        encoding="utf-8",
    )
    return pkg


# ── Gap-fill pipeline ───────────────────────────────────────────────────────

def test_stub_body_produces_valid_python() -> None:
    src = _stub_body("my_gap", "explain things")
    assert "def my_gap(results: dict):" in src
    assert "return None" in src


def test_validate_synthesized_accepts_clean_stdlib() -> None:
    src = "import json\n\ndef transform(results: dict):\n    return json.dumps(results)\n"
    assert _validate_synthesized(src, "transform") is True


def test_validate_synthesized_rejects_third_party() -> None:
    src = "import requests\n\ndef transform(results: dict):\n    return requests.get('x')\n"
    assert _validate_synthesized(src, "transform") is False


def test_validate_synthesized_rejects_missing_function() -> None:
    src = "def something_else(x):\n    return x\n"
    assert _validate_synthesized(src, "my_gap") is False


def test_validate_synthesized_rejects_syntax_error() -> None:
    assert _validate_synthesized("def broken(", "broken") is False


def test_gap_fill_pipeline_fills_with_stub_when_no_llm(tmp_path: Path) -> None:
    pkg = _make_pkg(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    ping_id = next(b.id for b in reg.all_blocks() if b.name == "ping")

    plan = CompositionPlan(
        name="one_gap",
        target_tier="a3_og_features",
        nodes=[CompositionNode(id=ping_id), CompositionNode(id="gap:wrap_output")],
        edges=[CompositionEdge(src=ping_id, dst="gap:wrap_output")],
        gaps=[Gap(slug="wrap_output", referenced_by=["gap:wrap_output"], hint="wrap the result")],
    )
    pipeline = GapFillPipeline(reg, allow_stub_fallback=True, use_llm=False)
    report = pipeline.run(plan, target_root=pkg)

    assert report.final_verdict == "PASS"
    assert report.gaps_total == 1
    assert report.gaps_stubbed == 1
    assert report.gaps_failed == 0
    assert report.materialized_path == "a3_og_features/one_gap_feature.py"
    materialized = pkg / report.materialized_path
    assert materialized.is_file()
    # Must no longer reference gap stubs — real block was swapped in
    src = materialized.read_text(encoding="utf-8")
    assert "gap:" not in src
    assert "wrap_output" in src


def test_gap_fill_rejects_when_stub_disabled_and_no_llm(tmp_path: Path) -> None:
    pkg = _make_pkg(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    plan = CompositionPlan(
        name="no_stub",
        target_tier="a3_og_features",
        nodes=[CompositionNode(id="gap:only_thing")],
        gaps=[Gap(slug="only_thing", referenced_by=["gap:only_thing"])],
    )
    pipeline = GapFillPipeline(reg, allow_stub_fallback=False, use_llm=False)
    report = pipeline.run(plan, target_root=pkg)
    assert report.gaps_failed == 1


# ── Hot-patch runtime ───────────────────────────────────────────────────────

def test_module_for_path_maps_file_to_dotted_name(tmp_path: Path) -> None:
    pkg = _make_pkg(tmp_path)
    path = pkg / "a1_at_functions" / "ping.py"
    name = module_for_path(path)
    assert name == "demo_pkg.a1_at_functions.ping"


def test_module_for_path_returns_none_for_non_python(tmp_path: Path) -> None:
    f = tmp_path / "not_python.txt"
    f.write_text("hi", encoding="utf-8")
    assert module_for_path(f) is None


def test_reload_module_refuses_blocked_modules() -> None:
    blocked = next(iter(_BLOCKLIST))
    result = reload_module(blocked)
    assert result.status == "skipped_blocked"
    assert "refused" in result.error.lower()


def test_hot_patch_imports_fresh_module(tmp_path: Path) -> None:
    pkg = _make_pkg(tmp_path)
    path = pkg / "a1_at_functions" / "ping.py"
    # Ensure not pre-loaded (unique pkg name isolates us)
    sys.modules.pop("demo_pkg.a1_at_functions.ping", None)

    report = hot_patch([path], root=pkg)
    assert report.verdict == "PASS"
    assert len(report.results) == 1
    r = report.results[0]
    assert r.status in {"imported", "reloaded"}
    assert "demo_pkg.a1_at_functions.ping" in sys.modules


def test_hot_patch_reloads_already_loaded_module(tmp_path: Path) -> None:
    pkg = _make_pkg(tmp_path)
    path = pkg / "a1_at_functions" / "ping.py"

    # Prime the module into sys.modules
    sys.path.insert(0, str(pkg.parent))
    try:
        import importlib
        importlib.import_module("demo_pkg.a1_at_functions.ping")
        assert "demo_pkg.a1_at_functions.ping" in sys.modules

        report = hot_patch([path], root=pkg)
        assert report.verdict == "PASS"
        assert report.results[0].status == "reloaded"
    finally:
        sys.path.remove(str(pkg.parent))
        sys.modules.pop("demo_pkg.a1_at_functions.ping", None)


def test_hot_patch_reports_not_found_for_bad_path(tmp_path: Path) -> None:
    bogus = tmp_path / "nope.py"
    report = hot_patch([bogus], root=tmp_path)
    assert any(r.status == "not_found" for r in report.results)


# ── Server endpoints ────────────────────────────────────────────────────────

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402


def _server(working_dir: Path) -> TestClient:
    from ass_ade.a2_mo_composites.ag_ui_bus import reset_bus
    from ass_ade.a3_og_features.ag_ui_server import build_app

    reset_bus()
    return TestClient(build_app(working_dir=working_dir))


def test_server_synthesize_fills_and_materializes(tmp_path: Path) -> None:
    pkg_parent = tmp_path / "src"
    pkg_parent.mkdir()
    pkg = _make_pkg(pkg_parent)
    client = _server(tmp_path)

    blocks = client.get("/playground/blocks", params={"query": "ping"}).json()["blocks"]
    assert blocks
    ping_id = blocks[0]["id"]

    plan = {
        "name": "srv_with_gap",
        "target_tier": "a3_og_features",
        "nodes": [{"id": ping_id}, {"id": "gap:tag"}],
        "edges": [{"src": ping_id, "dst": "gap:tag"}],
        "gaps": [{"slug": "tag", "hint": "tag the result"}],
        "description": "server synth smoke",
    }
    r = client.post(
        "/playground/synthesize",
        json={"plan": plan, "use_llm": False, "allow_stub_fallback": True},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["final_verdict"] in {"PASS", "REFINE"}
    assert body["materialized_path"] == "a3_og_features/srv_with_gap_feature.py"
    assert (pkg / body["materialized_path"]).is_file()


def test_server_hot_patch_rejects_empty_paths(tmp_path: Path) -> None:
    client = _server(tmp_path)
    r = client.post("/playground/hot-patch", json={})
    assert r.status_code == 400


def test_server_hot_patch_loads_module(tmp_path: Path) -> None:
    pkg_parent = tmp_path / "src"
    pkg_parent.mkdir()
    pkg = _make_pkg(pkg_parent)
    client = _server(tmp_path)

    sys.modules.pop("demo_pkg.a1_at_functions.ping", None)
    r = client.post(
        "/playground/hot-patch",
        json={"paths": [str((pkg / "a1_at_functions" / "ping.py"))]},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] in {"PASS", "REFINE"}
    assert any(
        res["status"] in {"imported", "reloaded"}
        and res["module"] == "demo_pkg.a1_at_functions.ping"
        for res in body["results"]
    )


# ── @patch REPL meta-command ────────────────────────────────────────────────

def test_at_patch_handler_summarizes_reload(tmp_path: Path) -> None:
    from ass_ade.interpreter import Atomadic, _handle_at_command

    pkg_parent = tmp_path / "src"
    pkg_parent.mkdir()
    pkg = _make_pkg(pkg_parent)
    sys.modules.pop("demo_pkg.a1_at_functions.ping", None)

    agent = Atomadic(working_dir=pkg)
    out = _handle_at_command(
        agent, "patch", str((pkg / "a1_at_functions" / "ping.py"))
    )
    assert "Hot-patch" in out
    assert "PASS" in out or "REFINE" in out


def test_at_patch_handler_shows_usage_when_empty(tmp_path: Path) -> None:
    from ass_ade.interpreter import Atomadic, _handle_at_command

    agent = Atomadic(working_dir=tmp_path)
    out = _handle_at_command(agent, "patch", "")
    assert "Usage" in out
    assert "@patch" in out
