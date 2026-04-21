"""Kotlin -> Python regex-based transpiler."""

from __future__ import annotations

import re

from ass_ade.engine.transpile.base import TranspileClass, TranspileFunction
from ass_ade.engine.transpile._regex_base import (
    RegexTranspiler,
    extract_balanced_block,
    mask_ranges,
    split_params,
)

_IMPORT_RE = re.compile(r"^\s*import\s+([A-Za-z_][\w\.]*)", re.MULTILINE)
_FUNC_RE = re.compile(
    r"""
    (?P<modifiers>(?:\b(?:public|private|internal|protected|open|override|final|abstract|suspend|inline|operator)\b\s*)*)
    fun\s+
    (?:<[^>]*>\s*)?
    (?:[A-Za-z_][\w\.]*\.)?  # extension receiver
    (?P<name>[A-Za-z_][\w]*)\s*
    \(\s*(?P<params>[^)]*?)\s*\)
    \s*(?::\s*(?P<ret>[^\{=]+?))?
    \s*(?:=\s*[^\n\{]+|\{)
    """,
    re.VERBOSE,
)
_CLASS_RE = re.compile(
    r"""
    (?:data\s+|sealed\s+|abstract\s+|open\s+|inner\s+|enum\s+|annotation\s+)*
    (?:class|object|interface)\s+(?P<name>[A-Za-z_][\w]*)
    (?:<[^>]*>)?
    (?:\s*\((?P<primary>[^)]*)\))?
    (?:\s*:\s*(?P<bases>[^\{]+))?
    \s*\{
    """,
    re.VERBOSE,
)


class KotlinTranspiler(RegexTranspiler):
    """Regex-based Kotlin scanner."""

    language = "kotlin"
    file_extensions = (".kt", ".kts")

    def scan(self, source: str):
        imports = tuple(sorted(set(_IMPORT_RE.findall(source))))
        classes_with_ranges = list(self._extract_classes_with_ranges(source))
        class_ranges = [r for _, r in classes_with_ranges]
        classes = tuple(c for c, _ in classes_with_ranges)
        masked = mask_ranges(source, class_ranges)
        functions = tuple(self._extract_functions(masked))
        warnings: tuple[str, ...] = ()
        if not functions and not classes:
            warnings = ("no kotlin declarations extracted",)
        return functions, classes, imports, warnings

    def _extract_functions(self, source: str):
        for m in _FUNC_RE.finditer(source):
            body = ""
            end_idx = m.end()
            if source[end_idx - 1] == "{":
                _, body = extract_balanced_block(source, end_idx - 1)
            yield TranspileFunction(
                name=m.group("name"),
                params=_kotlin_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=body.strip(),
                is_async="suspend" in (m.group("modifiers") or ""),
            )

    def _extract_classes_with_ranges(self, source: str):
        for m in _CLASS_RE.finditer(source):
            brace_idx = m.end() - 1
            end, body = extract_balanced_block(source, brace_idx)
            bases: tuple[str, ...] = ()
            if m.group("bases"):
                bases = tuple(
                    b.split("(")[0].strip()
                    for b in m.group("bases").split(",")
                    if b.strip()
                )
            fields = tuple(self._extract_fields(body, m.group("primary")))
            methods = tuple(self._extract_methods(body))
            yield (
                TranspileClass(
                    name=m.group("name"),
                    bases=bases,
                    fields=fields,
                    methods=methods,
                ),
                (brace_idx, end),
            )

    def _extract_fields(self, body: str, primary: str | None) -> list[str]:
        fields: list[str] = []
        if primary:
            for p in split_params(primary):
                parts = p.split(":")
                if parts:
                    name_tokens = parts[0].split()
                    if name_tokens:
                        fields.append(name_tokens[-1])
        prop_re = re.compile(
            r"\b(?:public|private|internal|protected|open|override|final)?\s*(?:val|var)\s+([A-Za-z_][\w]*)"
        )
        fields.extend(m.group(1) for m in prop_re.finditer(body))
        return fields

    def _extract_methods(self, body: str):
        for m in _FUNC_RE.finditer(body):
            mbody = ""
            if body[m.end() - 1] == "{":
                _, mbody = extract_balanced_block(body, m.end() - 1)
            yield TranspileFunction(
                name=m.group("name"),
                params=_kotlin_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=mbody.strip(),
                is_async="suspend" in (m.group("modifiers") or ""),
                is_method=True,
            )


def _kotlin_params(params_src: str) -> list[str]:
    """Kotlin params: ``val name: Type = default``."""
    out: list[str] = []
    for raw in split_params(params_src):
        if ":" in raw:
            left, right = raw.split(":", 1)
            tokens = left.split()
            name = tokens[-1] if tokens else left.strip()
            ann = right.split("=")[0].strip()
            out.append(f"{name}: {ann}")
        else:
            out.append(raw.strip())
    return out
