from __future__ import annotations

from pathlib import Path

from ass_ade_v11.a1_at_functions.materialize_a0_plan import certify_a0_layout, layout_a0_files
from ass_ade_v11.a0_qk_constants.pipeline_meta import MINI_REBUILD_MATERIAL_SCHEMA
from ass_ade_v11.a4_sy_orchestration.run_phases_0_2_a0 import run_book_phases_0_2_a0


def test_e2e_mini_rebuild_writes_a0_and_stable_certificate(
    minimal_pkg_root: Path, tmp_path: Path
) -> None:
    tag = "e2e-pin-a0"
    book = run_book_phases_0_2_a0(
        minimal_pkg_root,
        tmp_path,
        rebuild_tag_a0=tag,
    )
    assert book["stopped_after"] == 2
    mat = book["a0_materialize"]
    assert mat is not None
    assert mat["summary"]["modules"] >= 1
    assert mat["certificate"]["material_schema"] == MINI_REBUILD_MATERIAL_SCHEMA
    target = Path(mat["target_root"])
    assert target.is_dir()
    py_files = list(target.glob("*.py"))
    assert len(py_files) == mat["summary"]["modules"]

    book2 = run_book_phases_0_2_a0(
        minimal_pkg_root,
        tmp_path / "second",
        rebuild_tag_a0=tag,
    )
    assert book2["a0_materialize"]["certificate"]["certificate_sha256"] == mat["certificate"][
        "certificate_sha256"
    ]


def test_a1_only_fixture_emits_zero_a0_modules(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parent / "fixtures" / "a1_only" / "example_pkg"
    book = run_book_phases_0_2_a0(root, tmp_path, rebuild_tag_a0="no-a0")
    assert book["stopped_after"] == 2
    mat = book["a0_materialize"]
    assert mat is not None
    assert mat["summary"]["modules"] == 0
    assert mat["certificate"]["module_count"] == 0


def test_certify_empty_layout_is_deterministic() -> None:
    c1 = certify_a0_layout({}, schema=MINI_REBUILD_MATERIAL_SCHEMA)
    c2 = certify_a0_layout({}, schema=MINI_REBUILD_MATERIAL_SCHEMA)
    assert c1["certificate_sha256"] == c2["certificate_sha256"]
    assert c1["manifest"] == {}


def test_layout_sorts_paths() -> None:
    props = [
        {
            "tier": "a0_qk_constants",
            "name": "zebra",
            "kind": "pure_function",
            "id": "a0.z",
            "dedup_key": "a0|zebra|COR",
            "source_symbol": {"path": "z.py", "line": 1},
        },
        {
            "tier": "a0_qk_constants",
            "name": "alpha",
            "kind": "pure_function",
            "id": "a0.a",
            "dedup_key": "a0|alpha|COR",
            "source_symbol": {"path": "a.py", "line": 2},
        },
    ]
    files = layout_a0_files(props)
    assert list(files.keys()) == sorted(files.keys())
