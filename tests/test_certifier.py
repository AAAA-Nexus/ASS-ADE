from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade.local.certifier import (
    build_local_certificate,
    compute_codebase_digest,
    hash_file,
    render_certificate_text,
)


# ---------------------------------------------------------------------------
# hash_file
# ---------------------------------------------------------------------------


def test_hash_file_deterministic(tmp_path: Path) -> None:
    f = tmp_path / "sample.py"
    f.write_bytes(b"def hello(): pass\n")

    h1 = hash_file(f)
    h2 = hash_file(f)

    assert h1 == h2
    assert len(h1) == 64  # sha256 hex digest length


def test_hash_file_different_content(tmp_path: Path) -> None:
    f1 = tmp_path / "a.py"
    f2 = tmp_path / "b.py"
    f1.write_bytes(b"x = 1")
    f2.write_bytes(b"x = 2")

    assert hash_file(f1) != hash_file(f2)


# ---------------------------------------------------------------------------
# compute_codebase_digest
# ---------------------------------------------------------------------------


def test_compute_codebase_digest_basic(tmp_path: Path) -> None:
    (tmp_path / "alpha.py").write_text("a = 1\n", encoding="utf-8")
    (tmp_path / "beta.py").write_text("b = 2\n", encoding="utf-8")

    result = compute_codebase_digest(tmp_path)

    assert "root_digest" in result
    assert result["file_count"] == 2
    assert "files" in result
    assert isinstance(result["files"], dict)


def test_compute_codebase_digest_ignores_pyc(tmp_path: Path) -> None:
    (tmp_path / "module.pyc").write_bytes(b"\x00\x01\x02")

    result = compute_codebase_digest(tmp_path)

    assert result["file_count"] == 0
    assert "module.pyc" not in result.get("files", {})


def test_compute_codebase_digest_deterministic(tmp_path: Path) -> None:
    (tmp_path / "stable.py").write_text("stable = True\n", encoding="utf-8")

    r1 = compute_codebase_digest(tmp_path)
    r2 = compute_codebase_digest(tmp_path)

    assert r1["root_digest"] == r2["root_digest"]


def test_compute_codebase_digest_changes_on_file_edit(tmp_path: Path) -> None:
    f = tmp_path / "mutable.py"
    f.write_text("version = 1\n", encoding="utf-8")

    r1 = compute_codebase_digest(tmp_path)

    f.write_text("version = 2\n", encoding="utf-8")

    r2 = compute_codebase_digest(tmp_path)

    assert r1["root_digest"] != r2["root_digest"]


# ---------------------------------------------------------------------------
# build_local_certificate
# ---------------------------------------------------------------------------


def test_build_local_certificate_structure(tmp_path: Path) -> None:
    (tmp_path / "src.py").write_text("pass\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path)

    for key in ("schema", "version", "digest", "signed_by", "valid"):
        assert key in cert, f"missing key: {key}"
    assert cert["signed_by"] is None
    assert cert["valid"] is False


def test_build_local_certificate_version(tmp_path: Path) -> None:
    (tmp_path / "src.py").write_text("pass\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path, version="1.2.3")

    assert cert["version"] == "1.2.3"


# ---------------------------------------------------------------------------
# render_certificate_text
# ---------------------------------------------------------------------------


def test_render_certificate_text_contains_digest(tmp_path: Path) -> None:
    (tmp_path / "code.py").write_text("x = 42\n", encoding="utf-8")

    cert = build_local_certificate(tmp_path)
    text = render_certificate_text(cert)

    root_digest = cert["digest"]["root_digest"]
    # The render function truncates to 32 chars
    assert root_digest[:32] in text
