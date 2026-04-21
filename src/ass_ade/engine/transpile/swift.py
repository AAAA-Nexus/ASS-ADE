"""Swift -> Python regex-based transpiler."""

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
    (?P<modifiers>(?:\b(?:public|private|internal|fileprivate|open|static|final|override|async|throws)\b\s*)*)
    func\s+(?P<name>[A-Za-z_][\w]*)\s*
    (?:<[^>]*>\s*)?
    \(\s*(?P<params>[^)]*?)\s*\)
    \s*(?:async\s*)?(?:throws\s*)?
    (?:->\s*(?P<ret>[^\{]+?))?
    \s*\{
    """,
    re.VERBOSE,
)
_CLASS_RE = re.compile(
    r"\b(?:class|struct|actor|protocol|enum)\s+(?P<name>[A-Za-z_][\w]*)"
    r"(?:\s*:\s*(?P<bases>[^\{]+))?\s*\{",
)


class SwiftTranspiler(RegexTranspiler):
    """Regex-based Swift scanner. Good enough for structural migration."""

    language = "swift"
    file_extensions = (".swift",)

    def scan(self, source: str):
        imports = tuple(sorted(set(_IMPORT_RE.findall(source))))
        classes_list = list(self._extract_classes_with_ranges(source))
        class_ranges = [cr for _, cr in classes_list]
        classes = tuple(c for c, _ in classes_list)
        masked = mask_ranges(source, class_ranges)
        functions = tuple(self._extract_functions(masked))
        warnings: tuple[str, ...] = ()
        if not functions and not classes:
            warnings = (
                "no swift functions or types extracted; source may use protocols/extensions outside regex coverage",
            )
        return functions, classes, imports, warnings

    def _extract_functions(self, source: str):
        for m in _FUNC_RE.finditer(source):
            brace_idx = m.end() - 1
            _, body = extract_balanced_block(source, brace_idx)
            yield TranspileFunction(
                name=m.group("name"),
                params=_swift_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=body.strip(),
                is_async="async" in (m.group("modifiers") or ""),
            )

    def _extract_classes_with_ranges(self, source: str):
        for m in _CLASS_RE.finditer(source):
            brace_idx = m.end() - 1
            end, body = extract_balanced_block(source, brace_idx)
            bases: tuple[str, ...] = ()
            if m.group("bases"):
                bases = tuple(b.strip() for b in m.group("bases").split(",") if b.strip())
            fields = tuple(self._extract_fields(body))
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

    def _extract_fields(self, body: str):
        field_re = re.compile(
            r"\b(?:public|private|internal|fileprivate|open|static)?\s*(?:let|var)\s+([A-Za-z_][\w]*)",
        )
        return [m.group(1) for m in field_re.finditer(body)]

    def _extract_methods(self, body: str):
        for m in _FUNC_RE.finditer(body):
            brace_idx = m.end() - 1
            _, mbody = extract_balanced_block(body, brace_idx)
            yield TranspileFunction(
                name=m.group("name"),
                params=_swift_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=mbody.strip(),
                is_async="async" in (m.group("modifiers") or ""),
                is_method=True,
            )


def _swift_params(params_src: str) -> list[str]:
    """Swift params can have argument labels: ``func f(label name: T)``.

    We keep only the internal ``name: T`` view because Python has no labels.
    """
    out: list[str] = []
    for raw in split_params(params_src):
        parts = raw.split(":", 1)
        if len(parts) == 2:
            left, right = parts
            tokens = left.split()
            name = tokens[-1] if tokens else left.strip()
            out.append(f"{name}: {right.strip()}")
        else:
            out.append(raw.strip())
    return out
