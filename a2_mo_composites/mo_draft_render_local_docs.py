# Extracted from C:/!ass-ade/src/ass_ade/local/docs_engine.py:268
# Component id: mo.source.ass_ade.render_local_docs
from __future__ import annotations

__version__ = "0.1.0"

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

    return written
