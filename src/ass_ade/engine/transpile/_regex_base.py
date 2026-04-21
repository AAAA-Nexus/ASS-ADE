"""Shared regex-based scanning helpers for non-Python transpilers.

This is a pragmatic first cut. The language-specific transpilers own the
regex patterns and the Python emission rules; this module provides the
brace-matching body extractor and the common Python emitter helpers.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from ass_ade.engine.transpile.base import (
    TranspileClass,
    TranspileFunction,
    TranspileResult,
    Transpiler,
    format_python_header,
    placeholder_body,
)


def extract_balanced_block(source: str, open_idx: int, open_ch: str = "{", close_ch: str = "}") -> tuple[int, str]:
    """Return ``(end_index, body)`` for a balanced ``{...}`` block.

    ``open_idx`` must point at the opening brace. If braces are unbalanced
    or missing, returns ``(open_idx, "")``.
    """
    if open_idx >= len(source) or source[open_idx] != open_ch:
        return open_idx, ""
    depth = 0
    in_string: str | None = None
    escape = False
    i = open_idx
    body_start = open_idx + 1
    while i < len(source):
        ch = source[i]
        if in_string is not None:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == in_string:
                in_string = None
            i += 1
            continue
        if ch in ('"', "'"):
            in_string = ch
            i += 1
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1, source[body_start:i]
        i += 1
    return open_idx, ""


def strip_line_comments(source: str, prefixes: Iterable[str] = ("//",)) -> str:
    """Strip line comments so pattern regexes don't accidentally match them.

    Keeps block comments intact (some languages nest them).
    """
    out_lines: list[str] = []
    for line in source.splitlines():
        cut = len(line)
        in_str: str | None = None
        escape = False
        for i, ch in enumerate(line):
            if in_str is not None:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == in_str:
                    in_str = None
                continue
            if ch in ('"', "'"):
                in_str = ch
                continue
            for pfx in prefixes:
                if line.startswith(pfx, i):
                    cut = i
                    break
            if cut != len(line):
                break
        out_lines.append(line[:cut].rstrip())
    return "\n".join(out_lines)


def mask_ranges(source: str, ranges: Iterable[tuple[int, int]]) -> str:
    """Replace the characters in each ``(start, end)`` range with spaces.

    Used by language scanners to blank out class bodies before looking for
    top-level functions, so nested methods are not picked up twice.
    """
    buf = list(source)
    for start, end in ranges:
        for i in range(max(0, start), min(len(buf), end)):
            if buf[i] != "\n":
                buf[i] = " "
    return "".join(buf)


def split_params(params_src: str) -> list[str]:
    """Split a parameter list by top-level commas (ignoring nested ``<>`` / ``()``).

    Returns params as raw language-specific text (e.g. ``"a: Int = 0"``).
    """
    params: list[str] = []
    depth = 0
    buf: list[str] = []
    for ch in params_src:
        if ch in "(<[{":
            depth += 1
        elif ch in ")>]}":
            depth -= 1
        if ch == "," and depth == 0:
            tok = "".join(buf).strip()
            if tok:
                params.append(tok)
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        params.append(tail)
    return params


class RegexTranspiler(Transpiler):
    """Base class that supplies a generic Python emitter for regex scanners.

    Subclasses must implement :meth:`scan` to return
    ``(functions, classes, imports, warnings)``.
    """

    comment_prefixes: tuple[str, ...] = ("//",)

    def scan(
        self, source: str
    ) -> tuple[
        tuple[TranspileFunction, ...],
        tuple[TranspileClass, ...],
        tuple[str, ...],
        tuple[str, ...],
    ]:
        raise NotImplementedError

    def transpile_source(
        self,
        source: str,
        *,
        source_path: str | Path | None = None,
    ) -> TranspileResult:
        cleaned = strip_line_comments(source, self.comment_prefixes)
        functions, classes, imports, warnings = self.scan(cleaned)
        header = format_python_header(
            source_language=self.language,
            source_path=str(source_path) if source_path else None,
            backend="regex",
            warnings=warnings,
        )
        body = self._emit_python(functions, classes, imports)
        return TranspileResult(
            source_language=self.language,
            source_path=str(source_path) if source_path else None,
            python_code=header + body,
            functions=functions,
            classes=classes,
            imports=imports,
            warnings=warnings,
            backend="regex",
        )

    def _emit_python(
        self,
        functions: tuple[TranspileFunction, ...],
        classes: tuple[TranspileClass, ...],
        imports: tuple[str, ...],
    ) -> str:
        parts: list[str] = []
        if imports:
            parts.append("# Imports preserved from source (as comments):")
            for imp in imports:
                parts.append(f"# - {imp}")
            parts.append("")
        for cls in classes:
            parts.append(_emit_class(cls))
            parts.append("")
        for fn in functions:
            parts.append(_emit_function(fn, indent=""))
            parts.append("")
        if not classes and not functions:
            parts.append("# No top-level declarations extracted.")
            parts.append("# The regex scanner may need tuning for this dialect;")
            parts.append("# consider enabling the tree-sitter backend.")
            parts.append("")
        return "\n".join(parts)


def _emit_function(fn: TranspileFunction, *, indent: str = "") -> str:
    def_kw = "async def" if fn.is_async else "def"
    sig_params = ", ".join(_python_params(fn.params))
    ret = f" -> {_python_type(fn.return_type)}" if fn.return_type else ""
    lines: list[str] = []
    for dec in fn.decorators:
        lines.append(f"{indent}# decorator (source): {dec}")
    lines.append(f"{indent}{def_kw} {fn.name}({sig_params}){ret}:")
    doc = fn.docstring or f"Transpiled {fn.name}."
    lines.append(f'{indent}    """{doc}"""')
    lines.append(placeholder_body(fn.body, indent=indent + "    "))
    return "\n".join(lines)


def _emit_class(cls: TranspileClass) -> str:
    lines: list[str] = []
    bases = ", ".join(cls.bases) if cls.bases else ""
    header = f"class {cls.name}({bases}):" if bases else f"class {cls.name}:"
    lines.append(header)
    doc = cls.docstring or f"Transpiled class {cls.name}."
    lines.append(f'    """{doc}"""')
    if cls.fields:
        for f in cls.fields:
            lines.append(f"    {f}: object  # field from source")
    if not cls.fields and not cls.methods:
        lines.append("    pass")
    for m in cls.methods:
        lines.append("")
        lines.append(_emit_function(m, indent="    "))
    return "\n".join(lines)


_PARAM_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


def _python_params(params: list[str]) -> list[str]:
    """Best-effort conversion of foreign params to Python params.

    We only keep names (plus optional annotations) - default values and
    complex generics are dropped.
    """
    out: list[str] = []
    for p in params:
        # Strip leading modifiers (swift "inout", typescript "readonly", etc.)
        tokens = p.replace(":", " : ").replace("=", " = ").split()
        # Typical shape: [modifier] name [: Type] [= default]
        name = None
        ann = None
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t in ("inout", "readonly", "val", "var", "const", "let", "mut", "ref"):
                i += 1
                continue
            if _PARAM_NAME_RE.fullmatch(t):
                name = t
                i += 1
                break
            i += 1
        if name is None:
            continue
        # Look for ":" for annotation
        if ":" in tokens[i:]:
            ann_idx = tokens.index(":", i)
            # Consume up to "=" or end
            end = len(tokens)
            if "=" in tokens[ann_idx:]:
                end = tokens.index("=", ann_idx)
            ann = "".join(tokens[ann_idx + 1 : end]).strip()
        py_type = _python_type(ann) if ann else None
        out.append(f"{name}: {py_type}" if py_type else name)
    return out


_TYPE_MAP = {
    "String": "str",
    "Int": "int",
    "Int32": "int",
    "Int64": "int",
    "UInt": "int",
    "Long": "int",
    "i32": "int",
    "i64": "int",
    "u32": "int",
    "u64": "int",
    "usize": "int",
    "Float": "float",
    "Double": "float",
    "f32": "float",
    "f64": "float",
    "Bool": "bool",
    "Boolean": "bool",
    "number": "float",
    "string": "str",
    "boolean": "bool",
    "any": "object",
    "Any": "object",
    "void": "None",
    "Void": "None",
    "Unit": "None",
    "Nothing": "None",
    "undefined": "None",
    "null": "None",
}


def _python_type(t: str | None) -> str:
    if not t:
        return "object"
    t = t.strip().rstrip(";").rstrip("?")  # swift/kotlin nullable suffix
    mapped = _TYPE_MAP.get(t)
    if mapped:
        return mapped
    # simple generic mapping: Array<T> / List<T> / Vec<T> -> list[T]
    m = re.match(r"(Array|List|Vec|Sequence|Iterable)<(.+)>$", t)
    if m:
        return f"list[{_python_type(m.group(2))}]"
    m = re.match(r"\[(.+)\]$", t)  # Swift [T]
    if m:
        return f"list[{_python_type(m.group(1))}]"
    m = re.match(r"(Dictionary|Map|HashMap|Record)<(.+),(.+)>$", t)
    if m:
        return f"dict[{_python_type(m.group(2))}, {_python_type(m.group(3))}]"
    m = re.match(r"\[(.+):(.+)\]$", t)  # Swift [K: V]
    if m:
        return f"dict[{_python_type(m.group(1))}, {_python_type(m.group(2))}]"
    return "object"
