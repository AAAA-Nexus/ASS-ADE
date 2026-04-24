"""Tier a1 — TypeScript symbol scanner: regex-based extraction of exported symbols from .ts/.tsx files."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

TsSymbolKind = Literal["function", "class", "interface", "type", "const", "method", "enum"]

_EXCLUDE_DIRS = frozenset({
    ".git", "node_modules", "dist", "build", ".next", ".turbo",
    "__pycache__", ".venv", "coverage", ".nyc_output",
})

# Matches top-level exports with capture groups: (async?)(kind)(name)
_EXPORT_RE = re.compile(
    r"^export\s+"
    r"(?P<default>default\s+)?"
    r"(?P<async>async\s+)?"
    r"(?P<kind>function\*?|class|abstract\s+class|interface|type|const|let|var|enum)\s+"
    r"(?P<name>[A-Za-z_$][A-Za-z0-9_$]*)",
    re.MULTILINE,
)

# Arrow-function export: export const name = (...) =>
_ARROW_RE = re.compile(
    r"^export\s+(?:const|let)\s+(?P<name>[A-Za-z_$][A-Za-z0-9_$]*)\s*[=:][^;{]*(?:=>|\()",
    re.MULTILINE,
)

# Method inside a class: optional modifiers + name + (
_METHOD_RE = re.compile(
    r"^\s+(?:(?:public|private|protected|static|async|override|readonly|abstract)\s+)*"
    r"(?P<name>[a-z_$][A-Za-z0-9_$]*)\s*(?:<[^>]*>)?\s*\(",
    re.MULTILINE,
)

_JSDOC_RE = re.compile(r"/\*\*[\s\S]*?\*/\s*$", re.MULTILINE)


@dataclass(frozen=True)
class TsSymbolRecord:
    """One discovered TypeScript symbol."""

    root: str
    rel_path: str
    module: str
    qualname: str
    kind: TsSymbolKind
    lineno: int
    end_lineno: int
    signature: str
    body_sha256: str
    docstring_present: bool
    is_exported: bool
    has_nearby_test: bool
    language: str = "typescript"
    decorators: tuple[str, ...] = field(default_factory=tuple)


def _is_excluded(rel: Path) -> bool:
    return any(part in _EXCLUDE_DIRS for part in rel.parts)


def _iter_ts_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in (".ts", ".tsx"):
            continue
        rel = path.relative_to(root)
        if _is_excluded(rel):
            continue
        # Skip generated declaration files
        if path.name.endswith(".d.ts"):
            continue
        files.append(path)
    return sorted(files)


def _module_name(root: Path, path: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    return "/".join(rel.parts)


def _body_hash(segment: str) -> str:
    return hashlib.sha256(segment.encode("utf-8")).hexdigest()[:16]


def _find_block_end(lines: list[str], start: int) -> int:
    """Walk forward from `start` tracking brace depth, return the closing line index."""
    depth = 0
    in_str: str | None = None
    for i in range(start, min(start + 300, len(lines))):
        for ch in lines[i]:
            if in_str:
                if ch == in_str:
                    in_str = None
            elif ch in ('"', "'", "`"):
                in_str = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i
    return min(start + 100, len(lines) - 1)


def _has_jsdoc_before(lines: list[str], lineno_0: int) -> bool:
    """Check for /** ... */ immediately before lineno_0 (0-based)."""
    i = lineno_0 - 1
    while i >= 0 and lines[i].strip() == "":
        i -= 1
    if i >= 0 and lines[i].strip().endswith("*/"):
        return True
    return False


def _test_names(root: Path) -> set[str]:
    names: set[str] = set()
    for pattern in ("**/*.test.ts", "**/*.spec.ts", "**/test/**/*.ts"):
        for path in root.glob(pattern):
            names.add(path.stem.replace(".test", "").replace(".spec", "").lower())
    return names


def scan_ts_symbols(root: str | Path) -> tuple[dict, list[TsSymbolRecord]]:
    """Scan TypeScript exports in root, return (summary_dict, records)."""
    resolved = Path(root).resolve()
    files = _iter_ts_files(resolved)
    known_tests = _test_names(resolved)
    symbols: list[TsSymbolRecord] = []

    for path in files:
        rel = path.relative_to(resolved)
        module = _module_name(resolved, path)
        # Skip test/spec files from the symbol list
        if any(part in ("test", "tests", "__tests__") for part in rel.parts):
            continue
        if ".test." in path.name or ".spec." in path.name:
            continue

        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        lines = source.splitlines()
        has_test = any(
            path.stem.lower() in known_tests or
            path.stem.lower().replace(".", "") in known_tests
            for _ in [1]
        )

        # Top-level exports
        for m in _EXPORT_RE.finditer(source):
            raw_kind = m.group("kind").strip()
            if "class" in raw_kind:
                kind: TsSymbolKind = "class"
            elif raw_kind.startswith("interface"):
                kind = "interface"
            elif raw_kind.startswith("type"):
                kind = "type"
            elif raw_kind.startswith("enum"):
                kind = "enum"
            elif raw_kind.startswith("function"):
                kind = "function"
            else:
                kind = "const"

            name = m.group("name")
            lineno = source[: m.start()].count("\n") + 1
            end_lineno = _find_block_end(lines, lineno - 1) + 1
            segment = "\n".join(lines[lineno - 1 : end_lineno])
            docstring = _has_jsdoc_before(lines, lineno - 1)

            symbols.append(
                TsSymbolRecord(
                    root=str(resolved),
                    rel_path=rel.as_posix(),
                    module=module,
                    qualname=name,
                    kind=kind,
                    lineno=lineno,
                    end_lineno=end_lineno,
                    signature=name,
                    body_sha256=_body_hash(segment),
                    docstring_present=docstring,
                    is_exported=True,
                    has_nearby_test=has_test,
                )
            )

            # For classes, also scan methods
            if kind == "class":
                class_lines = lines[lineno - 1 : end_lineno]
                class_src = "\n".join(class_lines)
                skip = {"constructor", "get", "set", "if", "for", "while", "switch", "catch"}
                for mm in _METHOD_RE.finditer(class_src):
                    mname = mm.group("name")
                    if mname in skip or mname.startswith("_"):
                        continue
                    mlineno_0 = lineno - 1 + class_src[: mm.start()].count("\n")
                    mend = _find_block_end(lines, mlineno_0) + 1
                    mseg = "\n".join(lines[mlineno_0 : mend])
                    symbols.append(
                        TsSymbolRecord(
                            root=str(resolved),
                            rel_path=rel.as_posix(),
                            module=module,
                            qualname=f"{name}.{mname}",
                            kind="method",
                            lineno=mlineno_0 + 1,
                            end_lineno=mend,
                            signature=f"{name}.{mname}",
                            body_sha256=_body_hash(mseg),
                            docstring_present=_has_jsdoc_before(lines, mlineno_0),
                            is_exported=True,
                            has_nearby_test=has_test,
                        )
                    )

        # Arrow function exports not caught by the main regex
        for m in _ARROW_RE.finditer(source):
            name = m.group("name")
            # Skip if already captured
            if any(s.qualname == name and s.rel_path == rel.as_posix() for s in symbols):
                continue
            lineno = source[: m.start()].count("\n") + 1
            end_lineno = _find_block_end(lines, lineno - 1) + 1
            segment = "\n".join(lines[lineno - 1 : end_lineno])
            symbols.append(
                TsSymbolRecord(
                    root=str(resolved),
                    rel_path=rel.as_posix(),
                    module=module,
                    qualname=name,
                    kind="function",
                    lineno=lineno,
                    end_lineno=end_lineno,
                    signature=name,
                    body_sha256=_body_hash(segment),
                    docstring_present=_has_jsdoc_before(lines, lineno - 1),
                    is_exported=True,
                    has_nearby_test=has_test,
                )
            )

    summary = {
        "ts_files": len(files),
        "symbols": len(symbols),
        "tested_symbols": sum(1 for s in symbols if s.has_nearby_test),
        "by_kind": _count_kinds(symbols),
    }
    return summary, symbols


def _count_kinds(symbols: list[TsSymbolRecord]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for s in symbols:
        counts[s.kind] = counts.get(s.kind, 0) + 1
    return counts
