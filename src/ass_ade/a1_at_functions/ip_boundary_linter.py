"""a1 pure IP-boundary linter.

Scans a given text buffer (already-read file contents) against the
forbidden-name, forbidden-regex, and forbidden-collocation rules defined
in ``!ass-ade/.ass-ade/lints/ip_boundary.yaml`` and emits structured
findings.

Tier: a1. Pure stateless functions. The CALLER performs all I/O
(reading the YAML config, reading the target file, walking a directory,
writing a report). This module is safe to import from any tier and
deterministic on its inputs.

Public surface:
    - ``Finding`` (frozen dataclass)
    - ``Severity`` (str enum)
    - ``lint_text(text, config, *, source_path="<buffer>") -> list[Finding]``
    - ``load_config_from_yaml_text(yaml_text) -> dict``  (uses stdlib only when
      available; falls back to a tiny parser for our own YAML shape)

Plan: autopoietic-ai-research-enhance-assade-r2-20260420-0212 (task T-E1a).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Sequence


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"


@dataclass(frozen=True)
class Finding:
    source_path: str
    line: int
    column: int
    severity: Severity
    rule: str
    match: str


def _compile_rules(
    rules: Sequence[dict[str, Any]],
) -> list[tuple[re.Pattern[str], Severity, str]]:
    compiled: list[tuple[re.Pattern[str], Severity, str]] = []
    for r in rules:
        pat_src = r["pattern"]
        sev = Severity(r["severity"])
        try:
            compiled.append((re.compile(pat_src), sev, pat_src))
        except re.error:
            compiled.append((re.compile(re.escape(pat_src)), sev, pat_src))
    return compiled


_RUST_TEST_MOD_RE = re.compile(r"^\s*#\[cfg\(test\)\]\s*$")
_RUST_MOD_CLOSE_RE = re.compile(r"^\s*\}\s*$")


def _test_block_lines(lines: Sequence[str]) -> set[int]:
    """Line numbers (1-indexed) that are inside a ``#[cfg(test)] mod ...``
    block. These lines are assumed to contain test-fixture text that is
    allowed to name forbidden terms for assert-absence purposes.

    The detector is Rust-specific; for non-Rust files it returns an empty
    set. It handles the single common pattern
    ``#[cfg(test)]\\nmod tests { ... }`` and tracks brace depth from the
    opening ``{`` to the matching ``}`` to avoid hand-rolling a full
    parser.
    """
    inside = set()
    depth = 0
    in_block = False
    for i, line in enumerate(lines, start=1):
        if not in_block:
            if _RUST_TEST_MOD_RE.match(line):
                in_block = True
                depth = 0
                continue
            continue
        if "{" in line:
            depth += line.count("{")
        if "}" in line:
            depth -= line.count("}")
        inside.add(i)
        if depth <= 0 and ("}" in line) and depth == 0 and "{" not in line:
            in_block = False
    return inside


def _scan(
    text: str,
    compiled: Sequence[tuple[re.Pattern[str], Severity, str]],
    source_path: str,
    rule_prefix: str,
    skip_lines: set[int] | None = None,
) -> list[Finding]:
    out: list[Finding] = []
    skip = skip_lines or set()
    for lineno, line in enumerate(text.splitlines(), start=1):
        if lineno in skip:
            continue
        for pat, sev, rule_src in compiled:
            for m in pat.finditer(line):
                out.append(
                    Finding(
                        source_path=source_path,
                        line=lineno,
                        column=m.start() + 1,
                        severity=sev,
                        rule=f"{rule_prefix}:{rule_src}",
                        match=m.group(0),
                    )
                )
    return out


def _scan_collocations(
    text: str,
    rules: Sequence[dict[str, Any]],
    source_path: str,
    skip_lines: set[int] | None = None,
) -> list[Finding]:
    out: list[Finding] = []
    skip = skip_lines or set()
    for r in rules:
        integers: Iterable[int] = r.get("integers", [])
        companions: Iterable[str] = r.get("companions", [])
        int_patterns = [re.compile(rf"\b{int(i)}\b") for i in integers]
        comp_re = re.compile("|".join(re.escape(c) for c in companions)) if companions else None
        if not comp_re:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if lineno in skip:
                continue
            if not comp_re.search(line):
                continue
            for ip in int_patterns:
                for m in ip.finditer(line):
                    out.append(
                        Finding(
                            source_path=source_path,
                            line=lineno,
                            column=m.start() + 1,
                            severity=Severity.CRITICAL,
                            rule=f"collocation:int={m.group(0)}+companion",
                            match=m.group(0),
                        )
                    )
    return out


def lint_text(
    text: str,
    config: dict[str, Any],
    *,
    source_path: str = "<buffer>",
    skip_rust_test_blocks: bool = True,
) -> list[Finding]:
    names = _compile_rules(config.get("forbidden_names", []))
    regexes = _compile_rules(config.get("forbidden_regex", []))
    lines = text.splitlines()
    skip: set[int] = set()
    if skip_rust_test_blocks and source_path.endswith(".rs"):
        skip = _test_block_lines(lines)
    out: list[Finding] = []
    out.extend(_scan(text, names, source_path, "name", skip_lines=skip))
    out.extend(_scan(text, regexes, source_path, "regex", skip_lines=skip))
    out.extend(
        _scan_collocations(
            text,
            config.get("forbidden_collocations", []),
            source_path,
            skip_lines=skip,
        )
    )
    return out


def load_config_from_yaml_text(yaml_text: str) -> dict[str, Any]:
    """Minimal YAML loader tailored to ``ip_boundary.yaml``.

    Uses ``PyYAML`` when importable; otherwise parses the subset used by
    the config file (top-level scalars, lists of inline flow mappings,
    lists of plain scalars).

    This intentionally keeps the linter importable in minimal venvs.
    """
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            return {}
        return data
    except ImportError:
        return _mini_yaml(yaml_text)


_FLOW_MAP_RE = re.compile(r"\{\s*(?P<body>[^{}]*?)\s*\}")


def _parse_flow_map(body: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for part in _split_top_level_commas(body):
        if ":" not in part:
            continue
        k, _, v = part.partition(":")
        key = k.strip()
        val_str = v.strip()
        out[key] = _coerce_scalar(val_str)
    return out


def _split_top_level_commas(s: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    buf: list[str] = []
    in_str: str | None = None
    for ch in s:
        if in_str:
            buf.append(ch)
            if ch == in_str:
                in_str = None
            continue
        if ch in ("'", '"'):
            in_str = ch
            buf.append(ch)
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf))
    return parts


def _coerce_scalar(v: str) -> Any:
    v = v.strip()
    if not v:
        return ""
    if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        items = [_coerce_scalar(p) for p in _split_top_level_commas(inner)]
        return items
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    if v in ("true", "True"):
        return True
    if v in ("false", "False"):
        return False
    return v


def _mini_yaml(yaml_text: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[Any] | None = None

    for raw_line in yaml_text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue

        if not line.startswith(" ") and line.endswith(":"):
            key = line[:-1].strip()
            current_key = key
            current_list = []
            out[key] = current_list
            continue

        if not line.startswith(" ") and ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = _coerce_scalar(v.strip())
            current_key = None
            current_list = None
            continue

        if line.lstrip().startswith("- ") and current_list is not None:
            item_str = line.lstrip()[2:].strip()
            m = _FLOW_MAP_RE.match(item_str)
            if m:
                current_list.append(_parse_flow_map(m.group("body")))
            else:
                current_list.append(_coerce_scalar(item_str))
            continue

    return out
