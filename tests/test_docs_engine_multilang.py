"""Tests for the Wave-3 multi-language doc generation additions."""

from __future__ import annotations

import pytest

from ass_ade.local.docs_engine import (
    build_local_analysis,
    render_api_reference,
    render_local_docs,
    scan_foreign_api,
    scan_python_api,
)


@pytest.fixture
def sample_project(tmp_path):
    """Create a tiny multi-language project used by the tests."""
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "demo"\nversion = "0.2.0"\ndescription = "demo"\n',
        encoding="utf-8",
    )
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "pkg" / "api.py").write_text(
        '"""Top module docs."""\n\n'
        "def add(a: int, b: int) -> int:\n"
        '    """Add two numbers."""\n'
        "    return a + b\n\n"
        "class Widget:\n"
        '    """A widget."""\n'
        "    def render(self, x: int) -> str:\n"
        '        """Render to string."""\n'
        "        return str(x)\n\n"
        "async def go(url: str) -> str:\n"
        '    """Fetch url."""\n'
        "    return url\n",
        encoding="utf-8",
    )
    (tmp_path / "ios").mkdir()
    (tmp_path / "ios" / "Model.swift").write_text(
        "import Foundation\n"
        "public struct Point {\n"
        "    let x: Int\n"
        "    let y: Int\n"
        "}\n"
        "public func greet(name: String) -> String {\n"
        '    return "Hi " + name\n'
        "}\n",
        encoding="utf-8",
    )
    (tmp_path / "web").mkdir()
    (tmp_path / "web" / "Widget.ts").write_text(
        'export class Widget { id: string; constructor(id: string) { this.id = id; } }\n'
        "export function add(a: number, b: number): number { return a + b; }\n",
        encoding="utf-8",
    )
    return tmp_path


class TestScanPythonApi:
    def test_returns_function_with_signature(self, sample_project):
        symbols = scan_python_api(sample_project)
        add = next(s for s in symbols if s["qualname"] == "add")
        assert add["kind"] == "function"
        assert "def add" in add["signature"]
        assert "int" in add["signature"]
        assert add["docstring"] == "Add two numbers."

    def test_captures_class_method_qualname(self, sample_project):
        symbols = scan_python_api(sample_project)
        render = next(s for s in symbols if s["qualname"] == "Widget.render")
        assert render["kind"] == "method"
        assert "Render to string." == render["docstring"]

    def test_async_flag(self, sample_project):
        symbols = scan_python_api(sample_project)
        go = next(s for s in symbols if s["qualname"] == "go")
        assert go["is_async"] is True
        assert go["signature"].startswith("async def go")

    def test_class_symbol_has_signature(self, sample_project):
        symbols = scan_python_api(sample_project)
        widget = next(s for s in symbols if s["qualname"] == "Widget")
        assert widget["kind"] == "class"
        assert widget["signature"] == "class Widget"

    def test_skips_venv(self, tmp_path):
        (tmp_path / ".venv").mkdir()
        (tmp_path / ".venv" / "bad.py").write_text("def _x(): ...", encoding="utf-8")
        (tmp_path / "good.py").write_text("def ok(): ...", encoding="utf-8")
        names = {s["name"] for s in scan_python_api(tmp_path)}
        assert "ok" in names
        assert "_x" not in names


class TestScanForeignApi:
    def test_swift_struct_and_function(self, sample_project):
        symbols = scan_foreign_api(sample_project)
        names = {(s["language"], s["kind"], s["name"]) for s in symbols}
        assert ("swift", "class", "Point") in names
        assert ("swift", "function", "greet") in names

    def test_typescript_class_and_function(self, sample_project):
        symbols = scan_foreign_api(sample_project)
        names = {(s["language"], s["kind"], s["name"]) for s in symbols}
        assert ("typescript", "class", "Widget") in names
        assert ("typescript", "function", "add") in names

    def test_language_tag_always_present(self, sample_project):
        symbols = scan_foreign_api(sample_project)
        assert all("language" in s for s in symbols)


class TestRenderApiReference:
    def test_contains_python_section(self, sample_project):
        analysis = build_local_analysis(sample_project)
        md = render_api_reference(analysis)
        assert md is not None
        assert "## Python" in md
        assert "def add(a: int, b: int) -> int" in md
        assert "Add two numbers." in md

    def test_contains_swift_section(self, sample_project):
        analysis = build_local_analysis(sample_project)
        md = render_api_reference(analysis)
        assert "## Swift" in md
        assert "class Point" in md

    def test_contains_typescript_section(self, sample_project):
        analysis = build_local_analysis(sample_project)
        md = render_api_reference(analysis)
        assert "## Typescript" in md
        assert "class Widget" in md

    def test_none_when_no_symbols(self, tmp_path):
        analysis = {"python_api": [], "foreign_api": [], "metadata": {}, "root": str(tmp_path)}
        assert render_api_reference(analysis) is None


class TestRenderLocalDocsWritesApiMd:
    def test_api_md_written_when_symbols_present(self, sample_project, tmp_path):
        analysis = build_local_analysis(sample_project)
        out = tmp_path / "docs_out"
        written = render_local_docs(analysis, out)
        assert "API.md" in written
        content = (out / "API.md").read_text(encoding="utf-8")
        assert "# demo API Reference" in content
        assert "def add" in content
        assert "class Point" in content

    def test_existing_docs_still_produced(self, sample_project, tmp_path):
        analysis = build_local_analysis(sample_project)
        out = tmp_path / "docs_out"
        written = render_local_docs(analysis, out)
        for f in ("README.md", "ARCHITECTURE.md", "FEATURES.md", "USER_GUIDE.md"):
            assert f in written
            assert (out / f).exists()

    def test_api_md_skipped_when_no_sources(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "empty"\nversion = "0.0.1"\n', encoding="utf-8"
        )
        analysis = build_local_analysis(tmp_path)
        out = tmp_path / "docs_out"
        written = render_local_docs(analysis, out)
        assert "API.md" not in written
