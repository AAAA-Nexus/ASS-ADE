"""Transpiler abstract base + result/error types.

A Transpiler subclass owns one (source_language -> target=python) lane.
The minimal contract is ``transpile_source(source: str) -> TranspileResult``.
Concrete implementations may opt into tree-sitter for richer AST work;
otherwise they fall back to regex scanning that is good enough to produce
structurally correct Python scaffolding with preserved bodies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class TranspileError(Exception):
    """Raised when a transpiler cannot process a source artifact."""


@dataclass(frozen=True)
class TranspileFunction:
    """A function/method extracted from a foreign source."""

    name: str
    params: list[str] = field(default_factory=list)
    return_type: str | None = None
    docstring: str | None = None
    body: str = ""
    is_async: bool = False
    is_method: bool = False
    decorators: tuple[str, ...] = ()


@dataclass(frozen=True)
class TranspileClass:
    """A class/struct/interface extracted from a foreign source."""

    name: str
    bases: tuple[str, ...] = ()
    fields: tuple[str, ...] = ()
    methods: tuple[TranspileFunction, ...] = ()
    docstring: str | None = None


@dataclass(frozen=True)
class TranspileResult:
    """Structured output of a single-file transpile run."""

    source_language: str
    source_path: str | None
    python_code: str
    functions: tuple[TranspileFunction, ...] = ()
    classes: tuple[TranspileClass, ...] = ()
    imports: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    backend: str = "regex"

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "source_language": self.source_language,
            "source_path": self.source_path,
            "python_code": self.python_code,
            "functions": [
                {
                    "name": f.name,
                    "params": list(f.params),
                    "return_type": f.return_type,
                    "docstring": f.docstring,
                    "is_async": f.is_async,
                    "is_method": f.is_method,
                    "decorators": list(f.decorators),
                }
                for f in self.functions
            ],
            "classes": [
                {
                    "name": c.name,
                    "bases": list(c.bases),
                    "fields": list(c.fields),
                    "methods": [m.name for m in c.methods],
                    "docstring": c.docstring,
                }
                for c in self.classes
            ],
            "imports": list(self.imports),
            "warnings": list(self.warnings),
            "backend": self.backend,
        }


class Transpiler(ABC):
    """Abstract transpiler lane. One subclass per source language."""

    language: str = "unknown"
    file_extensions: tuple[str, ...] = ()

    @abstractmethod
    def transpile_source(
        self,
        source: str,
        *,
        source_path: str | Path | None = None,
    ) -> TranspileResult:
        """Convert foreign source into a TranspileResult."""

    def transpile_file(self, path: str | Path) -> TranspileResult:
        """Read ``path`` and transpile it to Python."""
        p = Path(path)
        if not p.exists():
            raise TranspileError(f"source file not found: {p}")
        text = p.read_text(encoding="utf-8", errors="replace")
        return self.transpile_source(text, source_path=str(p))


def format_python_header(
    *,
    source_language: str,
    source_path: str | None,
    backend: str,
    warnings: tuple[str, ...] = (),
) -> str:
    """Build the standard auto-generated header for transpiled output."""
    lines = [
        '"""Auto-transpiled from {lang}.'.format(lang=source_language),
        "",
        "Source: {src}".format(src=source_path or "<inline>"),
        "Backend: {backend}".format(backend=backend),
    ]
    if warnings:
        lines.append("")
        lines.append("Warnings:")
        for w in warnings:
            lines.append(f"- {w}")
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    return "\n".join(lines)


def placeholder_body(body: str, indent: str = "    ") -> str:
    """Wrap a foreign body as a preserved comment block inside a Python stub."""
    if not body.strip():
        return f"{indent}raise NotImplementedError"
    commented = "\n".join(f"{indent}# {line}" for line in body.splitlines())
    return (
        f"{indent}# --- original body preserved ---\n"
        f"{commented}\n"
        f"{indent}# --- /original body ---\n"
        f"{indent}raise NotImplementedError"
    )
