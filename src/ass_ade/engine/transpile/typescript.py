"""TypeScript (and JavaScript) -> Python regex-based transpiler."""

from __future__ import annotations

import re

from ass_ade.engine.transpile.base import TranspileClass, TranspileFunction
from ass_ade.engine.transpile._regex_base import (
    RegexTranspiler,
    extract_balanced_block,
    mask_ranges,
)

_IMPORT_RE = re.compile(
    r"""import\s+(?:(?:\*\s+as\s+[A-Za-z_][\w]*)|[A-Za-z_][\w]*|\{[^}]*\})
        \s+from\s+['"]([^'"]+)['"]""",
    re.VERBOSE,
)
_REQUIRE_RE = re.compile(r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)")
_FUNC_RE = re.compile(
    r"""
    (?P<modifiers>(?:\b(?:export|async|public|private|protected|static)\b\s*)*)
    function\s+(?P<name>[A-Za-z_][\w]*)\s*
    (?:<[^>]*>\s*)?
    \(\s*(?P<params>[^)]*?)\s*\)
    \s*(?::\s*(?P<ret>[^\{=]+?))?
    \s*\{
    """,
    re.VERBOSE,
)
_ARROW_RE = re.compile(
    r"""
    (?:export\s+)?(?:const|let|var)\s+(?P<name>[A-Za-z_][\w]*)\s*
    (?::\s*[^=]+)?\s*=\s*
    (?P<async>async\s+)?\s*
    (?:<[^>]*>\s*)?
    \(\s*(?P<params>[^)]*?)\s*\)
    \s*(?::\s*(?P<ret>[^=]+?))?
    \s*=>\s*\{
    """,
    re.VERBOSE,
)
_CLASS_RE = re.compile(
    r"""
    (?:export\s+)?(?:abstract\s+)?class\s+(?P<name>[A-Za-z_][\w]*)
    (?:<[^>]*>)?
    (?:\s+extends\s+(?P<base>[A-Za-z_][\w\.]*))?
    (?:\s+implements\s+(?P<impls>[^\{]+))?
    \s*\{
    """,
    re.VERBOSE,
)


class TypeScriptTranspiler(RegexTranspiler):
    """Regex-based TypeScript / JavaScript scanner."""

    language = "typescript"
    file_extensions = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")

    def scan(self, source: str):
        imports = tuple(
            sorted(set(_IMPORT_RE.findall(source) + _REQUIRE_RE.findall(source)))
        )
        classes_with_ranges = list(self._extract_classes_with_ranges(source))
        class_ranges = [r for _, r in classes_with_ranges]
        classes = tuple(c for c, _ in classes_with_ranges)
        masked = mask_ranges(source, class_ranges)
        functions = list(self._extract_named_functions(masked))
        functions.extend(self._extract_arrow_functions(masked))
        warnings: tuple[str, ...] = ()
        if not functions and not classes:
            warnings = ("no TS/JS top-level declarations extracted",)
        return tuple(functions), classes, imports, warnings

    def _extract_named_functions(self, source: str):
        for m in _FUNC_RE.finditer(source):
            brace_idx = m.end() - 1
            _, body = extract_balanced_block(source, brace_idx)
            yield TranspileFunction(
                name=m.group("name"),
                params=_ts_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=body.strip(),
                is_async="async" in (m.group("modifiers") or ""),
            )

    def _extract_arrow_functions(self, source: str):
        for m in _ARROW_RE.finditer(source):
            brace_idx = m.end() - 1
            _, body = extract_balanced_block(source, brace_idx)
            yield TranspileFunction(
                name=m.group("name"),
                params=_ts_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=body.strip(),
                is_async=bool(m.group("async")),
            )

    def _extract_classes_with_ranges(self, source: str):
        for m in _CLASS_RE.finditer(source):
            brace_idx = m.end() - 1
            end, body = extract_balanced_block(source, brace_idx)
            bases = tuple(b for b in (m.group("base"),) if b)
            if m.group("impls"):
                bases = bases + tuple(
                    x.strip() for x in m.group("impls").split(",") if x.strip()
                )
            fields = tuple(_ts_fields(body))
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

    def _extract_methods(self, body: str):
        method_re = re.compile(
            r"""
            (?P<modifiers>(?:\b(?:public|private|protected|static|async|readonly)\b\s*)*)
            (?P<name>[A-Za-z_][\w]*)\s*
            (?:<[^>]*>\s*)?
            \(\s*(?P<params>[^)]*?)\s*\)
            \s*(?::\s*(?P<ret>[^\{=]+?))?
            \s*\{
            """,
            re.VERBOSE,
        )
        for m in method_re.finditer(body):
            name = m.group("name")
            if name in ("if", "for", "while", "switch", "catch", "function", "return", "class"):
                continue
            brace_idx = m.end() - 1
            _, mbody = extract_balanced_block(body, brace_idx)
            yield TranspileFunction(
                name=name,
                params=_ts_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=None,
                body=mbody.strip(),
                is_async="async" in (m.group("modifiers") or ""),
                is_method=True,
            )


def _ts_fields(body: str) -> list[str]:
    field_re = re.compile(
        r"^\s*(?:public|private|protected|readonly|static)?\s*"
        r"([A-Za-z_][\w]*)\s*[:?]\s*[^;=\n{]+[;=]",
        re.MULTILINE,
    )
    return [m.group(1) for m in field_re.finditer(body)]


def _ts_params(params_src: str) -> list[str]:
    """TS params: ``name: Type = default`` or ``name?: Type``."""
    out: list[str] = []
    from ass_ade.engine.transpile._regex_base import split_params

    for raw in split_params(params_src):
        if ":" in raw:
            name, ann = raw.split(":", 1)
            name = name.strip().rstrip("?")
            ann = ann.split("=")[0].strip()
            out.append(f"{name}: {ann}")
        else:
            out.append(raw.split("=")[0].strip().rstrip("?"))
    return out
