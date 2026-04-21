from __future__ import annotations

"""Local codebase analysis engine for documentation generation.

Analyzes any repo without network calls. Returns structured data
that the CLI layer forwards to the Nexus API for synthesis.

Wave 3 additions
----------------
- :func:`scan_python_api` - AST walk that captures full function / class
  signatures, docstrings, and line ranges (not just names).
- :func:`scan_foreign_api` - uses :mod:`ass_ade.engine.transpile` to pull
  Swift / TypeScript / Kotlin / Rust symbols into the same shape.
- :func:`render_api_reference` - emits a proper ``API.md`` per-module.
- ``render_local_docs`` now writes ``API.md`` when any symbols carry
  signature metadata.
"""

import ast
import os
import re
from pathlib import Path
from typing import Any

from ass_ade.local.repo import DEFAULT_IGNORED_DIRS, summarize_repo


def detect_languages(root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for dirpath, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in DEFAULT_IGNORED_DIRS]
        for filename in files:
            suffix = Path(filename).suffix.lstrip(".").lower()
            if suffix:
                counts[suffix] = counts.get(suffix, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True))


def load_project_metadata(root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source": None,
        "name": None,
        "version": None,
        "description": None,
        "dependencies": [],
        "entry_points": [],
        "license": None,
        "language_hint": None,
    }

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        result["source"] = "pyproject.toml"
        result["language_hint"] = "python"
        try:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib  # type: ignore[no-reattr]
            data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            project = data.get("project", {})
            result["name"] = project.get("name")
            result["version"] = project.get("version")
            result["description"] = project.get("description")
            result["license"] = project.get("license")
            result["dependencies"] = project.get("dependencies", [])
            scripts = project.get("scripts", {})
            result["entry_points"] = list(scripts.keys())
            return result
        except Exception:
            pass
        # regex fallback
        try:
            raw = pyproject.read_text(encoding="utf-8")
            for field in ("name", "version", "description"):
                m = re.search(rf'^{field}\s*=\s*"([^"]+)"', raw, re.MULTILINE)
                if m:
                    result[field] = m.group(1)
        except Exception:
            pass
        return result

    for filename in ("setup.py", "setup.cfg"):
        candidate = root / filename
        if candidate.exists():
            result["source"] = filename
            result["language_hint"] = "python"
            try:
                raw = candidate.read_text(encoding="utf-8")
                for field in ("name", "version"):
                    m = re.search(rf'{field}\s*=\s*["\']([^"\']+)["\']', raw)
                    if m:
                        result[field] = m.group(1)
            except Exception:
                pass
            return result

    package_json = root / "package.json"
    if package_json.exists():
        result["source"] = "package.json"
        result["language_hint"] = "javascript"
        try:
            import json
            data = json.loads(package_json.read_text(encoding="utf-8"))
            result["name"] = data.get("name")
            result["version"] = data.get("version")
            result["description"] = data.get("description")
            deps = list(data.get("dependencies", {}).keys())
            deps += list(data.get("devDependencies", {}).keys())
            result["dependencies"] = deps
            result["entry_points"] = list(data.get("scripts", {}).keys())
            result["license"] = data.get("license")
        except Exception:
            pass
        return result

    cargo = root / "Cargo.toml"
    if cargo.exists():
        result["source"] = "Cargo.toml"
        result["language_hint"] = "rust"
        try:
            try:
                import tomllib
            except ImportError:
                import tomli as tomllib  # type: ignore[no-reattr]
            data = tomllib.loads(cargo.read_text(encoding="utf-8"))
            pkg = data.get("package", {})
            result["name"] = pkg.get("name")
            result["version"] = pkg.get("version")
            result["description"] = pkg.get("description")
        except Exception:
            pass
        return result

    go_mod = root / "go.mod"
    if go_mod.exists():
        result["source"] = "go.mod"
        result["language_hint"] = "go"
        try:
            raw = go_mod.read_text(encoding="utf-8")
            m = re.search(r"^module\s+(\S+)", raw, re.MULTILINE)
            if m:
                result["name"] = m.group(1)
            m = re.search(r"^go\s+(\S+)", raw, re.MULTILINE)
            if m:
                result["version"] = m.group(1)
        except Exception:
            pass
        return result

    return result


def scan_source_symbols(root: Path, max_files: int = 200) -> list[dict[str, Any]]:
    _def_re = re.compile(r"^(?:async\s+)?def\s+([A-Za-z_]\w*)")
    _class_re = re.compile(r"^class\s+([A-Za-z_]\w*)")
    symbols: list[dict[str, Any]] = []
    files_seen = 0

    _ignored = DEFAULT_IGNORED_DIRS | {".venv"}

    for dirpath, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in _ignored]
        for filename in files:
            if not filename.endswith(".py"):
                continue
            if files_seen >= max_files:
                break
            files_seen += 1
            full_path = Path(dirpath) / filename
            try:
                rel = str(full_path.relative_to(root))
                for line in full_path.read_text(encoding="utf-8", errors="replace").splitlines():
                    stripped = line.lstrip()
                    m = _class_re.match(stripped)
                    if m:
                        symbols.append({"file": rel, "kind": "class", "name": m.group(1)})
                        continue
                    m = _def_re.match(stripped)
                    if m:
                        symbols.append({"file": rel, "kind": "function", "name": m.group(1)})
            except Exception:
                pass

    return symbols


def scan_python_api(root: Path, max_files: int = 400) -> list[dict[str, Any]]:
    """AST-based API extraction for Python sources.

    Returns a list of symbol records with:
      ``{"file": str, "kind": "function"|"class"|"method",
        "name": str, "qualname": str, "signature": str,
        "docstring": str|None, "lineno": int, "is_async": bool}``
    """
    _ignored = DEFAULT_IGNORED_DIRS | {".venv", "venv", "build", "dist"}
    out: list[dict[str, Any]] = []
    seen = 0

    for dirpath, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in _ignored]
        for filename in files:
            if not filename.endswith(".py"):
                continue
            if seen >= max_files:
                return out
            seen += 1
            full = Path(dirpath) / filename
            try:
                rel = str(full.relative_to(root)).replace("\\", "/")
                source = full.read_text(encoding="utf-8", errors="replace")
                tree = ast.parse(source)
            except Exception:
                continue
            for node in tree.body:
                _collect_python_symbol(node, rel, qualname_prefix="", results=out)
    return out


def _collect_python_symbol(
    node: ast.AST,
    rel: str,
    *,
    qualname_prefix: str,
    results: list[dict[str, Any]],
) -> None:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        qualname = f"{qualname_prefix}{node.name}" if qualname_prefix else node.name
        results.append(
            {
                "file": rel,
                "kind": "method" if qualname_prefix else "function",
                "name": node.name,
                "qualname": qualname,
                "signature": _python_signature(node),
                "docstring": ast.get_docstring(node),
                "lineno": node.lineno,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
            }
        )
    elif isinstance(node, ast.ClassDef):
        qualname = f"{qualname_prefix}{node.name}" if qualname_prefix else node.name
        bases = [ast.unparse(b) for b in node.bases]
        results.append(
            {
                "file": rel,
                "kind": "class",
                "name": node.name,
                "qualname": qualname,
                "signature": f"class {qualname}({', '.join(bases)})" if bases else f"class {qualname}",
                "docstring": ast.get_docstring(node),
                "lineno": node.lineno,
                "is_async": False,
            }
        )
        for child in node.body:
            _collect_python_symbol(
                child, rel, qualname_prefix=f"{qualname}.", results=results
            )


def _python_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args_src = ast.unparse(node.args)
    ret = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    kw = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    return f"{kw} {node.name}({args_src}){ret}"


_FOREIGN_EXT = {
    ".swift": "swift",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".rs": "rust",
}


def scan_foreign_api(root: Path, max_files: int = 200) -> list[dict[str, Any]]:
    """Multi-language symbol extraction via the transpile engine.

    Walks ``root``, dispatches each recognized non-Python source through the
    appropriate :class:`Transpiler`, and flattens its functions / classes
    into the same symbol shape as :func:`scan_python_api`.
    """
    try:
        from ass_ade.engine.transpile import get_transpiler
    except Exception:
        return []

    _ignored = DEFAULT_IGNORED_DIRS | {
        ".venv",
        "venv",
        "node_modules",
        "target",
        "build",
        "dist",
    }
    out: list[dict[str, Any]] = []
    seen = 0
    for dirpath, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if d not in _ignored]
        for filename in files:
            ext = Path(filename).suffix.lower()
            lang = _FOREIGN_EXT.get(ext)
            if lang is None:
                continue
            if seen >= max_files:
                return out
            seen += 1
            full = Path(dirpath) / filename
            try:
                rel = str(full.relative_to(root)).replace("\\", "/")
                source = full.read_text(encoding="utf-8", errors="replace")
                result = get_transpiler(lang).transpile_source(source, source_path=rel)
            except Exception:
                continue
            for f in result.functions:
                params = ", ".join(f.params)
                ret = f" -> {f.return_type}" if f.return_type else ""
                kw = "async fn" if f.is_async else "fn"
                out.append(
                    {
                        "file": rel,
                        "kind": "function",
                        "name": f.name,
                        "qualname": f.name,
                        "signature": f"{kw} {f.name}({params}){ret}",
                        "docstring": f.docstring,
                        "lineno": 0,
                        "is_async": f.is_async,
                        "language": lang,
                    }
                )
            for cls in result.classes:
                base_txt = f"({', '.join(cls.bases)})" if cls.bases else ""
                out.append(
                    {
                        "file": rel,
                        "kind": "class",
                        "name": cls.name,
                        "qualname": cls.name,
                        "signature": f"class {cls.name}{base_txt}",
                        "docstring": cls.docstring,
                        "lineno": 0,
                        "is_async": False,
                        "language": lang,
                    }
                )
                for m in cls.methods:
                    params = ", ".join(m.params)
                    ret = f" -> {m.return_type}" if m.return_type else ""
                    kw = "async fn" if m.is_async else "fn"
                    out.append(
                        {
                            "file": rel,
                            "kind": "method",
                            "name": m.name,
                            "qualname": f"{cls.name}.{m.name}",
                            "signature": f"{kw} {cls.name}.{m.name}({params}){ret}",
                            "docstring": m.docstring,
                            "lineno": 0,
                            "is_async": m.is_async,
                            "language": lang,
                        }
                    )
    return out


def detect_test_framework(root: Path) -> str | None:
    if (root / "pytest.ini").exists():
        return "pytest"

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            raw = pyproject.read_text(encoding="utf-8")
            if "[tool.pytest" in raw:
                return "pytest"
        except Exception:
            pass

    for name in ("jest.config.js", "jest.config.ts", "jest.config.mjs", "jest.config.cjs"):
        if (root / name).exists():
            return "jest"

    cargo = root / "Cargo.toml"
    if cargo.exists():
        try:
            raw = cargo.read_text(encoding="utf-8")
            if "[dev-dependencies]" in raw:
                return "cargo-test"
        except Exception:
            pass

    if (root / "go.mod").exists():
        return "go-test"

    return None


def detect_ci(root: Path) -> list[str]:
    found: list[str] = []

    workflows_dir = root / ".github" / "workflows"
    if workflows_dir.exists():
        try:
            if any(p.suffix in {".yml", ".yaml"} for p in workflows_dir.iterdir()):
                found.append("github-actions")
        except Exception:
            pass

    if (root / ".gitlab-ci.yml").exists():
        found.append("gitlab-ci")

    if (root / "Jenkinsfile").exists():
        found.append("jenkins")

    if (root / ".circleci" / "config.yml").exists():
        found.append("circleci")

    return found


def build_local_analysis(root: Path) -> dict[str, Any]:
    resolved = root.resolve()
    analysis: dict[str, Any] = {"root": str(resolved)}
    try:
        analysis["languages"] = detect_languages(resolved)
    except Exception:
        analysis["languages"] = {}
    try:
        analysis["metadata"] = load_project_metadata(resolved)
    except Exception:
        analysis["metadata"] = {}
    try:
        analysis["symbols"] = scan_source_symbols(resolved)
    except Exception:
        analysis["symbols"] = []
    try:
        analysis["python_api"] = scan_python_api(resolved)
    except Exception:
        analysis["python_api"] = []
    try:
        analysis["foreign_api"] = scan_foreign_api(resolved)
    except Exception:
        analysis["foreign_api"] = []
    try:
        analysis["test_framework"] = detect_test_framework(resolved)
    except Exception:
        analysis["test_framework"] = None
    try:
        analysis["ci"] = detect_ci(resolved)
    except Exception:
        analysis["ci"] = []
    try:
        summary = summarize_repo(resolved)
        analysis["summary"] = {
            "total_files": summary.total_files,
            "total_dirs": summary.total_dirs,
            "file_types": summary.file_types,
            "top_level_entries": summary.top_level_entries,
        }
    except Exception:
        analysis["summary"] = {}
    return analysis


def render_local_docs(analysis: dict[str, Any], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}

    meta: dict[str, Any] = analysis.get("metadata") or {}
    symbols: list[dict[str, Any]] = analysis.get("symbols") or []
    languages: dict[str, int] = analysis.get("languages") or {}
    ci: list[str] = analysis.get("ci") or []
    test_fw = analysis.get("test_framework")
    summary: dict[str, Any] = analysis.get("summary") or {}
    entry_points: list[str] = meta.get("entry_points") or []
    lang_hint: str = meta.get("language_hint") or (next(iter(languages), None) or "unknown")
    project_name: str = meta.get("name") or Path(analysis.get("root", "project")).name
    version: str = meta.get("version") or "0.1.0"
    description: str = meta.get("description") or ""

    classes = [s for s in symbols if s["kind"] == "class"][:20]
    functions = [s for s in symbols if s["kind"] == "function"][:20]

    lang_badge = f"![Language]({lang_hint})" if lang_hint else ""
    test_badge = f"![Tests]({test_fw})" if test_fw else ""

    install_line = ""
    if lang_hint == "python":
        install_line = "pip install ."
    elif lang_hint == "javascript":
        install_line = "npm install"
    elif lang_hint == "rust":
        install_line = "cargo build --release"
    elif lang_hint == "go":
        install_line = "go build ./..."

    quickstart_lines = []
    if install_line:
        quickstart_lines.append(f"```\n{install_line}\n```")
    if entry_points:
        quickstart_lines.append(f"```\n{entry_points[0]} --help\n```")

    top_classes_md = "\n".join(f"- `{c['name']}` ({c['file']})" for c in classes) or "_none detected_"
    top_funcs_md = "\n".join(f"- `{f['name']}` ({f['file']})" for f in functions) or "_none detected_"

    readme = f"""# {project_name}

{description}

**Version:** {version}
{lang_badge} {test_badge}

## Installation

{chr(10).join(quickstart_lines) if quickstart_lines else "_See project documentation._"}

## Entry Points

{chr(10).join(f"- `{ep}`" for ep in entry_points) or "_none detected_"}

## Key Classes

{top_classes_md}

## Key Functions

{top_funcs_md}

## CI

{chr(10).join(f"- {c}" for c in ci) or "_none detected_"}
"""
    written["README.md"] = _write(output_dir / "README.md", readme)

    top_dirs = summary.get("top_level_entries") or []
    mermaid_nodes = "\n    ".join(f"root --> {d}" for d in top_dirs[:12])
    arch = f"""# Architecture

## Repository Overview

- **Total files:** {summary.get("total_files", "?")}
- **Total directories:** {summary.get("total_dirs", "?")}
- **Primary language:** {lang_hint}
- **Detected languages:** {", ".join(languages.keys())}

## Top-Level Structure

```mermaid
flowchart TD
    root[{project_name}]
    {mermaid_nodes}
```

## Entry Points

{chr(10).join(f"- `{ep}`" for ep in entry_points) or "_none detected_"}

## Test Framework

{test_fw or "_none detected_"}

## CI Systems

{chr(10).join(f"- {c}" for c in ci) or "_none detected_"}
"""
    written["ARCHITECTURE.md"] = _write(output_dir / "ARCHITECTURE.md", arch)

    by_file: dict[str, list[dict[str, Any]]] = {}
    for s in symbols:
        by_file.setdefault(s["file"], []).append(s)

    features_sections: list[str] = []
    for filepath, syms in list(by_file.items())[:30]:
        lines = [f"### `{filepath}`", ""]
        for s in syms:
            lines.append(f"- **{s['kind']}** `{s['name']}`")
        features_sections.append("\n".join(lines))

    features = f"""# Features

Extracted from {len(by_file)} source files.

{chr(10).join(features_sections)}
"""
    written["FEATURES.md"] = _write(output_dir / "FEATURES.md", features)

    user_guide = f"""# User Guide

## Installation

{chr(10).join(quickstart_lines) if quickstart_lines else "_See project documentation._"}

## Quickstart

1. Install the project using the command above.
2. Run `{entry_points[0] if entry_points else project_name} --help` to see available commands.
3. Consult ARCHITECTURE.md for a structural overview.

## Common Tasks

| Task | Command |
|------|---------|
| Install | `{install_line or "see docs"}` |
| Run tests | `{_test_command(lang_hint, test_fw)}` |
| Build | `{_build_command(lang_hint)}` |

## Configuration

Configuration is typically discovered automatically. See the project README for environment-specific options.
"""
    written["USER_GUIDE.md"] = _write(output_dir / "USER_GUIDE.md", user_guide)

    gitignore = _gitignore_for(lang_hint, languages)
    written[".gitignore"] = _write(output_dir / ".gitignore", gitignore)

    contributing = f"""# Contributing

Thank you for your interest in contributing to **{project_name}**!

## Getting Started

1. Fork the repository and clone it locally.
2. Install dependencies: `{install_line or "see README"}`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes, add tests where applicable.
5. Run the test suite: `{_test_command(lang_hint, test_fw)}`
6. Commit with a clear message and open a pull request.

## Code Style

- Follow the existing code style and conventions.
- Keep functions focused and single-purpose.
- Document non-obvious logic with comments that explain *why*, not *what*.

## Reporting Issues

Open a GitHub issue with reproduction steps and expected vs. actual behavior.
"""
    written["CONTRIBUTING.md"] = _write(output_dir / "CONTRIBUTING.md", contributing)

    changelog = f"""# Changelog

All notable changes to **{project_name}** will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

### Changed

### Fixed

### Removed
"""
    written["CHANGELOG.md"] = _write(output_dir / "CHANGELOG.md", changelog)

    api_md = render_api_reference(analysis)
    if api_md is not None:
        written["API.md"] = _write(output_dir / "API.md", api_md)

    return written


def render_api_reference(analysis: dict[str, Any]) -> str | None:
    """Render a full API reference from ``python_api`` + ``foreign_api``.

    Returns ``None`` if no signature-carrying symbols were captured.
    """
    py_api: list[dict[str, Any]] = analysis.get("python_api") or []
    foreign_api: list[dict[str, Any]] = analysis.get("foreign_api") or []
    if not py_api and not foreign_api:
        return None

    meta: dict[str, Any] = analysis.get("metadata") or {}
    project_name: str = meta.get("name") or Path(analysis.get("root", "project")).name
    version: str = meta.get("version") or "0.1.0"

    sections: list[str] = [
        f"# {project_name} API Reference",
        "",
        f"**Version:** {version}",
        "",
        "Auto-generated from source using AST analysis (Python) and the",
        "ASS-ADE transpile engine (Swift, TypeScript, Kotlin, Rust).",
        "",
    ]

    if py_api:
        sections.append("## Python")
        sections.append("")
        sections.extend(_render_api_group(py_api, language_label=None))

    if foreign_api:
        by_lang: dict[str, list[dict[str, Any]]] = {}
        for s in foreign_api:
            by_lang.setdefault(s.get("language", "unknown"), []).append(s)
        for lang in sorted(by_lang):
            sections.append(f"## {lang.capitalize()}")
            sections.append("")
            sections.extend(_render_api_group(by_lang[lang], language_label=lang))

    return "\n".join(sections).rstrip() + "\n"


def _render_api_group(
    symbols: list[dict[str, Any]],
    *,
    language_label: str | None,
) -> list[str]:
    by_file: dict[str, list[dict[str, Any]]] = {}
    for s in symbols:
        by_file.setdefault(s["file"], []).append(s)
    lines: list[str] = []
    for filepath in sorted(by_file):
        lines.append(f"### `{filepath}`")
        lines.append("")
        items = sorted(by_file[filepath], key=lambda r: (r.get("lineno", 0), r["qualname"]))
        for sym in items:
            kind = sym.get("kind", "symbol")
            qualname = sym.get("qualname", sym.get("name", "?"))
            sig = sym.get("signature") or qualname
            lineno = sym.get("lineno")
            loc = f" — line {lineno}" if lineno else ""
            lines.append(f"#### `{qualname}` _({kind})_{loc}")
            lines.append("")
            lines.append("```python" if language_label is None else f"```{language_label}")
            lines.append(sig)
            lines.append("```")
            lines.append("")
            doc = sym.get("docstring")
            if doc:
                lines.append(doc.strip())
                lines.append("")
        lines.append("")
    return lines


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def _test_command(lang_hint: str, test_fw: str | None) -> str:
    if test_fw == "pytest" or lang_hint == "python":
        return "pytest"
    if test_fw == "jest" or lang_hint == "javascript":
        return "npm test"
    if test_fw == "cargo-test" or lang_hint == "rust":
        return "cargo test"
    if test_fw == "go-test" or lang_hint == "go":
        return "go test ./..."
    return "see README"


def _build_command(lang_hint: str) -> str:
    if lang_hint == "python":
        return "pip install -e ."
    if lang_hint == "javascript":
        return "npm run build"
    if lang_hint == "rust":
        return "cargo build --release"
    if lang_hint == "go":
        return "go build ./..."
    return "see README"


def _gitignore_for(lang_hint: str, languages: dict[str, int]) -> str:
    sections: list[str] = ["# Generated by ass-ade docs", ""]
    has = lambda ext: ext in languages  # noqa: E731

    if lang_hint == "python" or has("py"):
        sections += [
            "# Python",
            "__pycache__/",
            "*.py[cod]",
            "*.pyo",
            ".venv/",
            "venv/",
            "dist/",
            "build/",
            "*.egg-info/",
            ".pytest_cache/",
            ".mypy_cache/",
            ".ruff_cache/",
            "",
        ]
    if lang_hint == "javascript" or has("js") or has("ts"):
        sections += [
            "# Node / JS",
            "node_modules/",
            "dist/",
            ".next/",
            ".nuxt/",
            "coverage/",
            "",
        ]
    if lang_hint == "rust" or has("rs"):
        sections += ["# Rust", "target/", "Cargo.lock", ""]
    if lang_hint == "go" or has("go"):
        sections += ["# Go", "*.exe", "*.test", "vendor/", ""]

    sections += ["# General", ".DS_Store", "Thumbs.db", ".env", "*.log", ""]
    return "\n".join(sections)
