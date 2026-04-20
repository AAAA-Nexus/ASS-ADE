from __future__ import annotations

import json
from pathlib import Path

import pytest

from ass_ade.local.docs_engine import (
    build_local_analysis,
    detect_ci,
    detect_languages,
    detect_test_framework,
    load_project_metadata,
    render_local_docs,
    scan_source_symbols,
)


# ---------------------------------------------------------------------------
# detect_languages
# ---------------------------------------------------------------------------


def test_detect_languages_on_tmp(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("pass", encoding="utf-8")
    (tmp_path / "utils.py").write_text("pass", encoding="utf-8")
    (tmp_path / "README.md").write_text("# hi", encoding="utf-8")

    result = detect_languages(tmp_path)

    assert result.get("py") == 2
    assert result.get("md") == 1


def test_detect_languages_ignores_venv(tmp_path: Path) -> None:
    venv = tmp_path / ".venv" / "lib"
    venv.mkdir(parents=True)
    (venv / "something.py").write_text("pass", encoding="utf-8")
    # Also add a real py file so the dict is non-empty in a different ext
    (tmp_path / "real.txt").write_text("x", encoding="utf-8")

    result = detect_languages(tmp_path)

    assert "py" not in result, ".venv .py files should be excluded"


# ---------------------------------------------------------------------------
# load_project_metadata
# ---------------------------------------------------------------------------


def test_load_project_metadata_pyproject(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "myproject"\nversion = "1.2.3"\ndescription = "A test project"\n',
        encoding="utf-8",
    )

    meta = load_project_metadata(tmp_path)

    assert meta["name"] == "myproject"
    assert meta["version"] == "1.2.3"
    assert meta["description"] == "A test project"


def test_load_project_metadata_package_json(tmp_path: Path) -> None:
    pkg = tmp_path / "package.json"
    pkg.write_text(
        json.dumps({"name": "my-pkg", "version": "2.0.0", "description": "js package"}),
        encoding="utf-8",
    )

    meta = load_project_metadata(tmp_path)

    assert meta["name"] == "my-pkg"
    assert meta["version"] == "2.0.0"


def test_load_project_metadata_empty(tmp_path: Path) -> None:
    meta = load_project_metadata(tmp_path)

    assert isinstance(meta, dict)
    # Should return a dict with None values, not raise
    assert "name" in meta


# ---------------------------------------------------------------------------
# scan_source_symbols
# ---------------------------------------------------------------------------


def test_scan_source_symbols_finds_functions(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("def foo():\n    pass\n\nclass Bar:\n    pass\n", encoding="utf-8")

    symbols = scan_source_symbols(tmp_path)
    names = {s["name"] for s in symbols}

    assert "foo" in names
    assert "Bar" in names


def test_scan_source_symbols_skips_venv(tmp_path: Path) -> None:
    venv_py = tmp_path / ".venv" / "lib"
    venv_py.mkdir(parents=True)
    (venv_py / "hidden.py").write_text("def secret(): pass\n", encoding="utf-8")

    symbols = scan_source_symbols(tmp_path)
    names = {s["name"] for s in symbols}

    assert "secret" not in names


# ---------------------------------------------------------------------------
# detect_test_framework
# ---------------------------------------------------------------------------


def test_detect_test_framework_pytest(tmp_path: Path) -> None:
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")

    result = detect_test_framework(tmp_path)

    assert result == "pytest"


# ---------------------------------------------------------------------------
# detect_ci
# ---------------------------------------------------------------------------


def test_detect_ci_github_actions(tmp_path: Path) -> None:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("on: push\n", encoding="utf-8")

    result = detect_ci(tmp_path)

    assert "github-actions" in result


# ---------------------------------------------------------------------------
# build_local_analysis
# ---------------------------------------------------------------------------


def test_build_local_analysis_returns_dict(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text("def main(): pass\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )

    analysis = build_local_analysis(tmp_path)

    assert isinstance(analysis, dict)
    for key in ("root", "languages", "metadata", "symbols", "test_framework", "ci", "summary"):
        assert key in analysis, f"missing key: {key}"


# ---------------------------------------------------------------------------
# render_local_docs
# ---------------------------------------------------------------------------


_EXPECTED_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "FEATURES.md",
    "USER_GUIDE.md",
    ".gitignore",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
]


def _minimal_analysis(tmp_path: Path) -> dict:
    """Build minimal analysis dict for render tests."""
    (tmp_path / "src.py").write_text("def hello(): pass\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "testpkg"\nversion = "0.0.1"\n',
        encoding="utf-8",
    )
    return build_local_analysis(tmp_path)


def test_render_local_docs_writes_files(tmp_path: Path) -> None:
    src_dir = tmp_path / "project"
    src_dir.mkdir()
    out_dir = tmp_path / "out"

    analysis = _minimal_analysis(src_dir)
    written = render_local_docs(analysis, out_dir)

    for name in _EXPECTED_FILES:
        assert name in written, f"{name} not in written dict"
        assert (out_dir / name).exists(), f"{name} not written to disk"


def test_render_local_docs_readme_contains_name(tmp_path: Path) -> None:
    src_dir = tmp_path / "project"
    src_dir.mkdir()
    out_dir = tmp_path / "out"

    analysis = _minimal_analysis(src_dir)
    render_local_docs(analysis, out_dir)

    readme = (out_dir / "README.md").read_text(encoding="utf-8")
    assert "testpkg" in readme
