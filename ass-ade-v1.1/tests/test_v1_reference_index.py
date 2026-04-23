from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade_v11.a0_qk_constants.reference_roots import ASS_ADE_V1_REFERENCE_ROOT_ENV
from ass_ade_v11.a1_at_functions.v1_reference_index import (
    attach_v1_reference_index,
    index_reference_root,
    resolve_ass_ade_v1_reference_root,
)
from ass_ade_v11.a3_og_features.pipeline_book import run_book_until


def test_index_reference_root_detects_manifest(tmp_path: Path) -> None:
    (tmp_path / "MANIFEST.json").write_text("{}", encoding="utf-8")
    idx = index_reference_root(tmp_path)
    assert idx["manifest_json"] is True
    assert idx["certificate_json"] is False


def test_run_book_includes_reference_block(minimal_pkg_root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ASS_ADE_V1_REFERENCE_ROOT_ENV, raising=False)
    monkeypatch.setenv(ASS_ADE_V1_REFERENCE_ROOT_ENV, str(minimal_pkg_root))
    book = run_book_until(minimal_pkg_root, None, stop_after=1)
    assert "reference_ass_ade_v1" in book
    ref = book["reference_ass_ade_v1"]
    assert ref.get("indexed") is True
    assert ref.get("root")


def test_resolve_none_when_path_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ASS_ADE_V1_REFERENCE_ROOT_ENV, "/nonexistent/ass-ade-v1-root-xyz")
    assert resolve_ass_ade_v1_reference_root() is None


def test_attach_marks_unindexed_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ASS_ADE_V1_REFERENCE_ROOT_ENV, "/nonexistent/ass-ade-v1-root-xyz")
    book = attach_v1_reference_index({"stopped_after": 0})
    assert book["reference_ass_ade_v1"]["indexed"] is False
