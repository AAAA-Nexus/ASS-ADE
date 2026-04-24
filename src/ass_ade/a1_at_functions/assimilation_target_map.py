"""Pure target mapping for selective sibling assimilation.

This module builds a dry-run map of sibling code before any rebuild or copy
step. It classifies discovered functions/classes into explicit actions so
operators can choose what to assimilate, rebuild, enhance, or skip.
"""

from __future__ import annotations

import ast
import datetime as dt
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

TargetAction = Literal["assimilate", "rebuild", "enhance", "skip"]
SymbolKind = Literal["function", "class", "method"]

_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site-packages",
}
_RISKY_IMPORTS = {"eval", "exec", "pickle", "subprocess", "socket", "telnetlib"}


@dataclass(frozen=True)
class SymbolRecord:
    root: str
    rel_path: str
    module: str
    qualname: str
    kind: SymbolKind
    lineno: int
    end_lineno: int
    signature: str
    body_sha256: str
    docstring_present: bool
    decorators: tuple[str, ...] = ()
    imports: tuple[str, ...] = ()
    has_nearby_test: bool = False


@dataclass(frozen=True)
class TargetDecision:
    action: TargetAction
    symbol: SymbolRecord
    matched_primary: SymbolRecord | None
    confidence: float
    reasons: tuple[str, ...] = ()
    recommended_path: str = ""


@dataclass(frozen=True)
class RootSummary:
    path: str
    python_files: int
    symbols: int
    tested_symbols: int


@dataclass(frozen=True)
class AssimilationTargetMap:
    schema_version: str
    generated_at_utc: str
    primary_root: str
    sibling_roots: tuple[str, ...]
    focus: tuple[str, ...]
    primary_summary: RootSummary
    sibling_summaries: tuple[RootSummary, ...]
    targets: tuple[TargetDecision, ...]
    action_counts: dict[str, int] = field(default_factory=dict)
    recommended_next_steps: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_excluded(path: Path) -> bool:
    return any(part in _EXCLUDE_DIRS for part in path.parts)


def _iter_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.py"):
        rel = path.relative_to(root)
        if _is_excluded(rel):
            continue
        files.append(path)
    return sorted(files)


def _module_name(root: Path, path: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = [part for part in rel.parts if part != "__init__"]
    return ".".join(parts)


def _args_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    parts: list[str] = []
    args = node.args
    all_pos = list(args.posonlyargs) + list(args.args)
    defaults_offset = len(all_pos) - len(args.defaults)
    for i, arg in enumerate(all_pos):
        prefix = "/" if i < len(args.posonlyargs) else ""
        suffix = "=" if i >= defaults_offset else ""
        parts.append(f"{prefix}{arg.arg}{suffix}")
    if args.vararg:
        parts.append(f"*{args.vararg.arg}")
    elif args.kwonlyargs:
        parts.append("*")
    kw_defaults = list(args.kw_defaults)
    for arg, default in zip(args.kwonlyargs, kw_defaults, strict=True):
        parts.append(f"{arg.arg}{'=' if default is not None else ''}")
    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")
    return f"({', '.join(parts)})"


def _decorator_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _decorator_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return ""


def _imports(tree: ast.AST) -> tuple[str, ...]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".", 1)[0])
    return tuple(sorted(names))


def _symbol_imports(module_imports: tuple[str, ...], node: ast.AST) -> tuple[str, ...]:
    referenced: set[str] = set()
    local_imports: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            referenced.add(child.id)
        elif isinstance(child, ast.Attribute) and isinstance(child.value, ast.Name):
            referenced.add(child.value.id)
        elif isinstance(child, ast.Import):
            local_imports.update(alias.name.split(".", 1)[0] for alias in child.names)
        elif isinstance(child, ast.ImportFrom) and child.module:
            local_imports.add(child.module.split(".", 1)[0])
    active = (set(module_imports) & referenced) | local_imports
    return tuple(sorted(active))


def _body_hash(source: str, node: ast.AST) -> str:
    segment = ast.get_source_segment(source, node) or ast.dump(node, include_attributes=False)
    return hashlib.sha256(segment.encode("utf-8")).hexdigest()


def _test_names(root: Path) -> set[str]:
    names: set[str] = set()
    tests_root = root / "tests"
    if not tests_root.is_dir():
        return names
    for path in _iter_python_files(tests_root):
        names.add(path.stem.removeprefix("test_"))
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.startswith("test_"):
                names.add(node.name.removeprefix("test_"))
    return names


def _symbol_tested(symbol: SymbolRecord, known_tests: set[str]) -> bool:
    leaf = symbol.qualname.split(".")[-1].lower()
    module_leaf = symbol.module.rsplit(".", 1)[-1].lower()
    return leaf in known_tests or module_leaf in known_tests


def scan_symbols(root: str | Path) -> tuple[RootSummary, tuple[SymbolRecord, ...]]:
    """Scan top-level Python functions/classes and class methods under ``root``."""
    resolved = Path(root).resolve()
    files = _iter_python_files(resolved)
    tests = {name.lower() for name in _test_names(resolved)}
    symbols: list[SymbolRecord] = []
    for path in files:
        if path.relative_to(resolved).parts[:1] == ("tests",):
            continue
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except (OSError, SyntaxError, UnicodeError):
            continue
        module = _module_name(resolved, path)
        imports = _imports(tree)
        rel_path = path.relative_to(resolved).as_posix()

        for node in tree.body:
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                record = SymbolRecord(
                    root=str(resolved),
                    rel_path=rel_path,
                    module=module,
                    qualname=node.name,
                    kind="function",
                    lineno=node.lineno,
                    end_lineno=getattr(node, "end_lineno", node.lineno),
                    signature=_args_signature(node),
                    body_sha256=_body_hash(source, node),
                    docstring_present=bool(ast.get_docstring(node)),
                    decorators=tuple(filter(None, (_decorator_name(d) for d in node.decorator_list))),
                    imports=_symbol_imports(imports, node),
                )
                symbols.append(
                    record.__class__(
                        **{**asdict(record), "has_nearby_test": _symbol_tested(record, tests)}
                    )
                )
            elif isinstance(node, ast.ClassDef):
                class_record = SymbolRecord(
                    root=str(resolved),
                    rel_path=rel_path,
                    module=module,
                    qualname=node.name,
                    kind="class",
                    lineno=node.lineno,
                    end_lineno=getattr(node, "end_lineno", node.lineno),
                    signature="class",
                    body_sha256=_body_hash(source, node),
                    docstring_present=bool(ast.get_docstring(node)),
                    decorators=tuple(filter(None, (_decorator_name(d) for d in node.decorator_list))),
                    imports=_symbol_imports(imports, node),
                )
                symbols.append(
                    class_record.__class__(
                        **{**asdict(class_record), "has_nearby_test": _symbol_tested(class_record, tests)}
                    )
                )
                for child in node.body:
                    if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
                        method = SymbolRecord(
                            root=str(resolved),
                            rel_path=rel_path,
                            module=module,
                            qualname=f"{node.name}.{child.name}",
                            kind="method",
                            lineno=child.lineno,
                            end_lineno=getattr(child, "end_lineno", child.lineno),
                            signature=_args_signature(child),
                            body_sha256=_body_hash(source, child),
                            docstring_present=bool(ast.get_docstring(child)),
                            decorators=tuple(
                                filter(None, (_decorator_name(d) for d in child.decorator_list))
                            ),
                            imports=_symbol_imports(imports, child),
                        )
                        symbols.append(
                            method.__class__(
                                **{**asdict(method), "has_nearby_test": _symbol_tested(method, tests)}
                            )
                        )
    summary = RootSummary(
        path=str(resolved),
        python_files=len(files),
        symbols=len(symbols),
        tested_symbols=sum(1 for symbol in symbols if symbol.has_nearby_test),
    )
    return summary, tuple(symbols)


def _risk_reasons(symbol: SymbolRecord) -> tuple[str, ...]:
    reasons: list[str] = []
    if symbol.qualname.startswith("_"):
        reasons.append("private symbol")
    if symbol.end_lineno - symbol.lineno > 160:
        reasons.append("large implementation")
    risky = sorted(set(symbol.imports) & _RISKY_IMPORTS)
    if risky:
        reasons.append(f"risky imports: {', '.join(risky)}")
    if not symbol.has_nearby_test:
        reasons.append("no nearby test evidence")
    return tuple(reasons)


def _matches_focus(symbol: SymbolRecord, focus: tuple[str, ...]) -> bool:
    if not focus:
        return True
    haystack = f"{symbol.module}.{symbol.qualname}".lower()
    return any(item.lower() in haystack for item in focus)


def _recommended_path(symbol: SymbolRecord, action: TargetAction) -> str:
    tier = "a1_at_functions" if symbol.kind == "function" else "a2_mo_composites"
    if action == "enhance":
        return f"enhance existing primary symbol matching {symbol.qualname}"
    if action == "rebuild":
        return f"rebuild as tiered component under src/ass_ade/{tier}/"
    if action == "assimilate":
        return f"assimilate candidate from {symbol.rel_path} into src/ass_ade/{tier}/"
    return "skip duplicate or out-of-scope symbol"


def classify_symbol(
    symbol: SymbolRecord,
    *,
    primary_by_qualname: dict[str, SymbolRecord],
    primary_by_leaf: dict[str, SymbolRecord],
) -> TargetDecision:
    """Classify one sibling symbol against the primary terrain."""
    exact = primary_by_qualname.get(symbol.qualname)
    leaf = symbol.qualname.rsplit(".", 1)[-1]
    loose = exact or primary_by_leaf.get(leaf)
    risks = _risk_reasons(symbol)

    if exact and exact.body_sha256 == symbol.body_sha256:
        action: TargetAction = "skip"
        reasons = ("same symbol body already exists in primary",)
        confidence = 0.98
    elif loose is not None:
        action = "enhance"
        reasons = (
            "primary has related symbol",
            "sibling may provide tests/docs/alternate behavior",
            *risks,
        )
        confidence = 0.78 if symbol.has_nearby_test or symbol.docstring_present else 0.62
    elif risks:
        action = "rebuild"
        reasons = ("new symbol needs tier-safe rebuild before assimilation", *risks)
        confidence = 0.70
    else:
        action = "assimilate"
        reasons = ("new tested/documented symbol with low static risk",)
        confidence = 0.84

    return TargetDecision(
        action=action,
        symbol=symbol,
        matched_primary=loose,
        confidence=confidence,
        reasons=tuple(reasons),
        recommended_path=_recommended_path(symbol, action),
    )


def build_assimilation_target_map(
    *,
    primary_root: str | Path,
    sibling_roots: list[str | Path],
    focus: list[str] | None = None,
) -> AssimilationTargetMap:
    """Build a selective target map for sibling feature growth."""
    primary_summary, primary_symbols = scan_symbols(primary_root)
    focus_tuple = tuple(item for item in (focus or []) if item.strip())
    primary_by_qualname = {symbol.qualname: symbol for symbol in primary_symbols}
    primary_by_leaf: dict[str, SymbolRecord] = {}
    for symbol in primary_symbols:
        primary_by_leaf.setdefault(symbol.qualname.rsplit(".", 1)[-1], symbol)

    sibling_summaries: list[RootSummary] = []
    targets: list[TargetDecision] = []
    for root in sibling_roots:
        summary, symbols = scan_symbols(root)
        sibling_summaries.append(summary)
        for symbol in symbols:
            if _matches_focus(symbol, focus_tuple):
                targets.append(
                    classify_symbol(
                        symbol,
                        primary_by_qualname=primary_by_qualname,
                        primary_by_leaf=primary_by_leaf,
                    )
                )

    counts = {action: 0 for action in ("assimilate", "rebuild", "enhance", "skip")}
    for target in targets:
        counts[target.action] += 1

    steps = (
        "Review rebuild targets first; they carry risk or missing test evidence.",
        "Feed assimilate/enhance candidates into policy-scoped `ass-ade assimilate` runs.",
        "Keep skip targets as provenance evidence; do not copy duplicate bodies.",
    )
    return AssimilationTargetMap(
        schema_version="ass-ade.assimilation-target-map/v1",
        generated_at_utc=dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        primary_root=str(Path(primary_root).resolve()),
        sibling_roots=tuple(str(Path(root).resolve()) for root in sibling_roots),
        focus=focus_tuple,
        primary_summary=primary_summary,
        sibling_summaries=tuple(sibling_summaries),
        targets=tuple(sorted(targets, key=lambda item: (item.action, item.symbol.module, item.symbol.qualname))),
        action_counts=counts,
        recommended_next_steps=steps,
    )


def dumps_target_map(target_map: AssimilationTargetMap) -> str:
    """Serialize a target map as stable, pretty JSON."""
    return json.dumps(target_map.to_dict(), indent=2, sort_keys=True) + "\n"
