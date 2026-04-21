"""Rust -> Python regex-based transpiler."""

from __future__ import annotations

import re

from ass_ade.engine.transpile.base import TranspileClass, TranspileFunction
from ass_ade.engine.transpile._regex_base import (
    RegexTranspiler,
    extract_balanced_block,
    mask_ranges,
    split_params,
)

_USE_RE = re.compile(r"^\s*use\s+([A-Za-z_][\w:]*)", re.MULTILINE)
_FUNC_RE = re.compile(
    r"""
    (?P<modifiers>(?:\b(?:pub|async|const|unsafe|extern)\b\s*(?:\([^)]+\)\s*)?)*)
    fn\s+(?P<name>[A-Za-z_][\w]*)\s*
    (?:<[^>]*>\s*)?
    \(\s*(?P<params>[^)]*?)\s*\)
    \s*(?:->\s*(?P<ret>[^\{;]+?))?
    \s*(?:where[^\{]+)?
    \s*\{
    """,
    re.VERBOSE,
)
_STRUCT_RE = re.compile(
    r"(?:pub\s+)?(?:struct|enum|trait|union)\s+(?P<name>[A-Za-z_][\w]*)"
    r"(?:<[^>]*>)?"
    r"(?:\s*:\s*(?P<bases>[^\{]+))?"
    r"\s*\{",
)


class RustTranspiler(RegexTranspiler):
    """Regex-based Rust scanner."""

    language = "rust"
    file_extensions = (".rs",)

    def scan(self, source: str):
        imports = tuple(sorted(set(_USE_RE.findall(source))))
        classes_with_ranges = list(self._extract_classes_with_ranges(source))
        class_ranges = [r for _, r in classes_with_ranges]
        classes = tuple(c for c, _ in classes_with_ranges)
        masked = mask_ranges(source, class_ranges)
        functions = tuple(self._extract_functions(masked))
        warnings: tuple[str, ...] = ()
        if not functions and not classes:
            warnings = ("no rust declarations extracted (impl blocks not yet parsed)",)
        return functions, classes, imports, warnings

    def _extract_functions(self, source: str):
        for m in _FUNC_RE.finditer(source):
            brace_idx = m.end() - 1
            _, body = extract_balanced_block(source, brace_idx)
            yield TranspileFunction(
                name=m.group("name"),
                params=_rust_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=body.strip(),
                is_async="async" in (m.group("modifiers") or ""),
            )

    def _extract_classes_with_ranges(self, source: str):
        for m in _STRUCT_RE.finditer(source):
            brace_idx = m.end() - 1
            end, body = extract_balanced_block(source, brace_idx)
            bases: tuple[str, ...] = ()
            if m.group("bases"):
                bases = tuple(
                    b.strip() for b in m.group("bases").split("+") if b.strip()
                )
            fields = tuple(_rust_fields(body))
            yield (
                TranspileClass(
                    name=m.group("name"),
                    bases=bases,
                    fields=fields,
                    methods=(),
                ),
                (brace_idx, end),
            )


def _rust_fields(body: str) -> list[str]:
    field_re = re.compile(
        r"(?:pub\s+(?:\([^)]+\)\s+)?)?([A-Za-z_][\w]*)\s*:\s*[^,\n]+[,\n]"
    )
    return [m.group(1) for m in field_re.finditer(body)]


def _rust_params(params_src: str) -> list[str]:
    out: list[str] = []
    for raw in split_params(params_src):
        if raw in ("&self", "&mut self", "self", "mut self"):
            out.append("self")
            continue
        if ":" in raw:
            left, right = raw.split(":", 1)
            tokens = left.replace("mut", "").replace("&", "").split()
            name = tokens[-1] if tokens else left.strip()
            out.append(f"{name}: {right.strip()}")
        else:
            out.append(raw.strip())
    return out
