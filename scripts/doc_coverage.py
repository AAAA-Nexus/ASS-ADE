#!/usr/bin/env python3
"""Report Python documentation coverage for ASS-ADE source files.

The checker is intentionally deterministic and local-only. It does not generate
docstrings; it tells agents exactly where documentation is missing so fixes stay
human-reviewed and grounded in the code.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_ROOTS = ("src/ass_ade", "scripts", "tools")
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
SKIP_PARTS = {
    "fixtures",
    "generated_smoke",
    ".ass-ade-pytest-basetemp",
}


@dataclass(frozen=True)
class MissingDoc:
    """One missing documentation item found by the coverage scan."""

    path: str
    kind: str
    name: str
    line: int


@dataclass(frozen=True)
class CoverageReport:
    """Serializable documentation coverage result."""

    roots: list[str]
    scanned_files: int
    missing: list[MissingDoc]

    @property
    def missing_count(self) -> int:
        """Return the number of missing doc entries."""
        return len(self.missing)


def iter_python_files(roots: Iterable[Path]) -> Iterable[Path]:
    """Yield Python files under roots while skipping caches and fixtures."""
    for root in roots:
        if root.is_file() and root.suffix == ".py":
            yield root
            continue
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root, topdown=True):
            current = Path(dirpath)
            dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
            if any(part in SKIP_PARTS for part in current.parts):
                dirnames[:] = []
                continue
            for filename in filenames:
                if filename.endswith(".py"):
                    yield current / filename


def public_name(name: str) -> bool:
    """Return whether a symbol should count toward public doc coverage."""
    return not name.startswith("_")


def scan_file(path: Path, repo_root: Path) -> list[MissingDoc]:
    """Return missing module and public symbol docstrings for one file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        rel = path.relative_to(repo_root).as_posix()
        return [MissingDoc(rel, "parse-error", str(exc), 1)]

    rel = path.relative_to(repo_root).as_posix()
    missing: list[MissingDoc] = []
    if ast.get_docstring(tree) is None:
        missing.append(MissingDoc(rel, "module", path.stem, 1))

    public_defs = (ast.AsyncFunctionDef, ast.FunctionDef)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and public_name(node.name):
            if ast.get_docstring(node) is None:
                missing.append(MissingDoc(rel, "class", node.name, node.lineno))
            for child in node.body:
                if isinstance(child, public_defs) and public_name(child.name):
                    if ast.get_docstring(child) is None:
                        missing.append(
                            MissingDoc(rel, "method", f"{node.name}.{child.name}", child.lineno)
                        )
        elif isinstance(node, public_defs) and public_name(node.name):
            if ast.get_docstring(node) is None:
                missing.append(MissingDoc(rel, "function", node.name, node.lineno))

    return missing


def build_report(repo_root: Path, roots: Iterable[Path]) -> CoverageReport:
    """Scan roots and return a documentation coverage report."""
    scanned = 0
    missing: list[MissingDoc] = []
    root_list = [root.resolve() for root in roots]
    for path in sorted(set(iter_python_files(root_list)), key=lambda p: p.as_posix().lower()):
        scanned += 1
        missing.extend(scan_file(path.resolve(), repo_root))
    return CoverageReport(
        roots=[path.relative_to(repo_root).as_posix() for path in root_list if path.exists()],
        scanned_files=scanned,
        missing=missing,
    )


def render_text(report: CoverageReport, limit: int) -> str:
    """Render a human-readable coverage summary."""
    lines = [
        "# Documentation Coverage",
        "",
        f"Scanned files: {report.scanned_files}",
        f"Missing entries: {report.missing_count}",
        "",
    ]
    if not report.missing:
        lines.append("All scanned public documentation targets are covered.")
        return "\n".join(lines)

    lines.append("## Missing")
    lines.append("")
    for item in report.missing[:limit]:
        lines.append(f"- {item.path}:{item.line} `{item.kind}` {item.name}")
    if report.missing_count > limit:
        lines.append(f"- ... {report.missing_count - limit} more")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the documentation coverage checker."""
    parser = argparse.ArgumentParser(description="Check ASS-ADE Python docstring coverage.")
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        help="Root or file to scan. Can be passed more than once.",
    )
    parser.add_argument("--json-out", type=Path, help="Write full coverage report as JSON.")
    parser.add_argument("--limit", type=int, default=80, help="Maximum missing entries to print.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any item is missing.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the documentation coverage checker."""
    args = parse_args()
    repo_root = Path.cwd().resolve()
    roots = [repo_root / p for p in (args.root or [Path(p) for p in DEFAULT_ROOTS])]
    report = build_report(repo_root, roots)

    print(render_text(report, args.limit))

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "roots": report.roots,
            "scanned_files": report.scanned_files,
            "missing_count": report.missing_count,
            "missing": [asdict(item) for item in report.missing],
        }
        args.json_out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if args.strict and report.missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
