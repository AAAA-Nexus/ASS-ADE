"""Tests for Phase D — Playground (block registry, composition, copilot)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade.a2_mo_composites.block_registry import BlockRegistry
from ass_ade.a3_og_features.atomadic_copilot import AtomadicCopilot, _offline_fallback_plan
from ass_ade.a3_og_features.composition_engine import (
    CompositionEdge,
    CompositionEngine,
    CompositionNode,
    CompositionPlan,
    Gap,
)


# ── Fixture: a tiny monadic source tree ─────────────────────────────────────

def _make_tree(root: Path) -> Path:
    pkg = root / "demo_pkg"
    for tier in (
        "a0_qk_constants", "a1_at_functions", "a2_mo_composites",
        "a3_og_features", "a4_sy_orchestration",
    ):
        (pkg / tier).mkdir(parents=True)
        (pkg / tier / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "__init__.py").write_text("", encoding="utf-8")

    (pkg / "a0_qk_constants" / "config.py").write_text(
        'VERSION = "1.0.0"\nDEFAULT_TIMEOUT = 30\n', encoding="utf-8",
    )
    (pkg / "a1_at_functions" / "parse_helpers.py").write_text(
        '"""Parse helpers."""\n\n'
        'def parse_input(text: str) -> dict:\n'
        '    """Parse a user text into a structured dict."""\n'
        '    return {"text": text}\n\n'
        'def _private_helper() -> None:\n'
        '    pass\n',
        encoding="utf-8",
    )
    (pkg / "a1_at_functions" / "format_helpers.py").write_text(
        '"""Format helpers."""\n\n'
        'def format_output(data: dict) -> str:\n'
        '    """Format a dict as a pretty string."""\n'
        '    return str(data)\n',
        encoding="utf-8",
    )
    (pkg / "a2_mo_composites" / "registry_core.py").write_text(
        '"""Registry core."""\n\n'
        'class RegistryCore:\n'
        '    """A stateful registry."""\n'
        '    def __init__(self):\n'
        '        self.items = []\n',
        encoding="utf-8",
    )
    return pkg


# ── BlockRegistry ───────────────────────────────────────────────────────────

def test_block_registry_scans_public_symbols(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    count = reg.scan()
    assert count >= 4
    stats = reg.stats()
    assert stats["by_tier"]["a0_qk_constants"] >= 2
    assert stats["by_tier"]["a1_at_functions"] >= 2
    assert stats["by_tier"]["a2_mo_composites"] >= 1
    names = {b.name for b in reg.all_blocks()}
    assert "parse_input" in names
    assert "format_output" in names
    assert "RegistryCore" in names
    assert "VERSION" in names  # constant
    assert "_private_helper" not in names  # leading underscore dropped


def test_block_registry_search_filters(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()

    by_query = reg.search(query="parse")
    assert any(b.name == "parse_input" for b in by_query)
    assert all("parse" in f"{b.name} {b.docstring}".lower() for b in by_query)

    by_tier = reg.search(tier="a1_at_functions")
    assert all(b.tier == "a1_at_functions" for b in by_tier)

    by_kind = reg.search(kind="class")
    assert all(b.kind == "class" for b in by_kind)
    assert any(b.name == "RegistryCore" for b in by_kind)


def test_block_registry_stable_ids(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg1 = BlockRegistry(pkg)
    reg1.scan()
    reg2 = BlockRegistry(pkg)
    reg2.scan()
    ids1 = sorted(b.id for b in reg1.all_blocks())
    ids2 = sorted(b.id for b in reg2.all_blocks())
    assert ids1 == ids2, "block ids must be deterministic across scans"


# ── CompositionEngine ───────────────────────────────────────────────────────

def test_composition_engine_emits_tier_correct_module(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    a1_blocks = [b for b in reg.by_tier("a1_at_functions") if b.kind == "function"]
    assert len(a1_blocks) >= 2

    plan = CompositionPlan(
        name="pipeline",
        target_tier="a3_og_features",
        nodes=[CompositionNode(id=a1_blocks[0].id), CompositionNode(id=a1_blocks[1].id)],
        edges=[CompositionEdge(src=a1_blocks[0].id, dst=a1_blocks[1].id)],
        description="Demo pipeline",
    )
    engine = CompositionEngine(reg)
    result = engine.compile(plan)
    assert result.verdict == "PASS"
    assert result.target_path == "a3_og_features/pipeline_feature.py"
    assert "from demo_pkg.a1_at_functions.parse_helpers" in result.source_code or \
           "from a1_at_functions.parse_helpers" in result.source_code
    assert "def pipeline(**context)" in result.source_code


def test_composition_rejects_upward_import(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    a2 = reg.by_tier("a2_mo_composites")[0]

    plan = CompositionPlan(
        name="bad",
        target_tier="a1_at_functions",  # lower than a2 — should violate
        nodes=[CompositionNode(id=a2.id)],
    )
    engine = CompositionEngine(reg)
    result = engine.compile(plan)
    assert result.verdict == "REJECT"
    assert any("cannot import upward" in v for v in result.tier_violations)


def test_composition_detects_gaps(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()

    plan = CompositionPlan(
        name="with_gap",
        target_tier="a3_og_features",
        nodes=[CompositionNode(id="gap:frobnicate")],
        gaps=[Gap(slug="frobnicate", referenced_by=["gap:frobnicate"], hint="twist the foo")],
    )
    engine = CompositionEngine(reg)
    result = engine.compile(plan)
    assert result.verdict == "REFINE"
    assert any(g.slug == "frobnicate" for g in result.detected_gaps)
    assert "def frobnicate" in result.source_code
    assert "NotImplementedError" in result.source_code


def test_composition_materialize_writes_parseable_source(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    a1 = [b for b in reg.by_tier("a1_at_functions") if b.kind == "function"]

    plan = CompositionPlan(
        name="materialized",
        target_tier="a3_og_features",
        nodes=[CompositionNode(id=a1[0].id)],
    )
    engine = CompositionEngine(reg)
    result = engine.compile(plan)
    result = engine.materialize(result, pkg)
    assert result.wrote_to_disk is True
    target_file = pkg / result.target_path
    assert target_file.is_file()
    import ast as _ast
    _ast.parse(target_file.read_text(encoding="utf-8"))  # must parse


def test_composition_topo_sort_detects_cycle(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    blocks = [b for b in reg.by_tier("a1_at_functions") if b.kind == "function"][:2]

    plan = CompositionPlan(
        name="cyclic",
        target_tier="a3_og_features",
        nodes=[CompositionNode(id=blocks[0].id), CompositionNode(id=blocks[1].id)],
        edges=[
            CompositionEdge(src=blocks[0].id, dst=blocks[1].id),
            CompositionEdge(src=blocks[1].id, dst=blocks[0].id),
        ],
    )
    result = CompositionEngine(reg).compile(plan)
    # Cycles are treated as hard failures (added to tier_violations)
    assert result.verdict == "REJECT"
    assert any("cycle" in v.lower() for v in result.tier_violations)


# ── AtomadicCopilot ─────────────────────────────────────────────────────────

def test_copilot_offline_fallback_matches_keywords(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()

    response = _offline_fallback_plan("parse and format text", reg)
    assert response.mode == "offline_fallback"
    assert response.suggested_plan is not None
    node_ids = [n["id"] for n in response.suggested_plan["nodes"]]
    # must include at least one of parse_input or format_output
    names = {reg.get(nid).name for nid in node_ids if reg.get(nid) is not None}
    assert names & {"parse_input", "format_output"}


def test_copilot_offline_fallback_empty_query(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    response = _offline_fallback_plan("", reg)
    # empty query → no tokens → returns a helpful note, no plan
    assert response.suggested_plan is None


def test_copilot_critique_detects_tier_violations(tmp_path: Path) -> None:
    pkg = _make_tree(tmp_path)
    reg = BlockRegistry(pkg)
    reg.scan()
    a2 = reg.by_tier("a2_mo_composites")[0]

    copilot = AtomadicCopilot(reg)
    critique = copilot.critique_plan({
        "name": "bad_plan",
        "target_tier": "a1_at_functions",
        "nodes": [{"id": a2.id}],
        "edges": [],
        "gaps": [],
    })
    assert critique.mode == "critique"
    assert "REJECT" in critique.text


# ── Server endpoints ───────────────────────────────────────────────────────

fastapi = pytest.importorskip("fastapi")


def _server(source_root: Path) -> TestClient:
    from fastapi.testclient import TestClient as _TestClient
    from ass_ade.a2_mo_composites.ag_ui_bus import reset_bus
    from ass_ade.a3_og_features.ag_ui_server import build_app

    reset_bus()
    return _TestClient(build_app(working_dir=source_root))


def test_server_playground_blocks_lists_registry(tmp_path: Path) -> None:
    pkg_root = tmp_path
    pkg = pkg_root / "src" / "demo_pkg"
    pkg.parent.mkdir(parents=True)
    _make_tree(pkg.parent)
    client = _server(pkg_root)
    r = client.get("/playground/blocks")
    assert r.status_code == 200
    body = r.json()
    assert body["stats"]["total_blocks"] >= 4
    names = {b["name"] for b in body["blocks"]}
    assert {"parse_input", "format_output", "RegistryCore"} <= names


def test_server_playground_blocks_search_query(tmp_path: Path) -> None:
    pkg_root = tmp_path
    pkg = pkg_root / "src" / "demo_pkg"
    pkg.parent.mkdir(parents=True)
    _make_tree(pkg.parent)
    client = _server(pkg_root)
    r = client.get("/playground/blocks", params={"query": "parse"})
    assert r.status_code == 200
    names = [b["name"] for b in r.json()["blocks"]]
    assert any("parse" in n for n in names)


def test_server_playground_compile_accepts_plan(tmp_path: Path) -> None:
    pkg_root = tmp_path
    pkg = pkg_root / "src" / "demo_pkg"
    pkg.parent.mkdir(parents=True)
    _make_tree(pkg.parent)
    client = _server(pkg_root)

    blocks = client.get("/playground/blocks", params={"tier": "a1_at_functions"}).json()["blocks"]
    assert blocks
    plan = {
        "name": "from_server",
        "target_tier": "a3_og_features",
        "nodes": [{"id": blocks[0]["id"]}],
        "edges": [],
        "gaps": [],
    }
    r = client.post("/playground/compile", json=plan)
    assert r.status_code == 200
    result = r.json()
    assert result["verdict"] in {"PASS", "REFINE"}
    assert result["target_path"] == "a3_og_features/from_server_feature.py"


def test_server_copilot_chat_returns_offline_when_no_llm(tmp_path: Path) -> None:
    pkg_root = tmp_path
    pkg = pkg_root / "src" / "demo_pkg"
    pkg.parent.mkdir(parents=True)
    _make_tree(pkg.parent)
    client = _server(pkg_root)

    r = client.post("/copilot/chat", json={"text": "parse and format some text"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] in {"llm", "offline_fallback"}
    # Whatever mode, we expect either text or a plan
    assert body["text"] or body.get("suggested_plan")


def test_server_copilot_reset(tmp_path: Path) -> None:
    pkg_root = tmp_path
    pkg = pkg_root / "src" / "demo_pkg"
    pkg.parent.mkdir(parents=True)
    _make_tree(pkg.parent)
    client = _server(pkg_root)
    r = client.post("/copilot/reset", json={})
    assert r.status_code == 200
    assert r.json() == {"ok": True}
