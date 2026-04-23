"""CNA-aware import rewrite for assimilated materialized trees (MAP = TERRAIN).

Maps ingested ``source_symbol.path`` + symbol names to materialized modules
``<tier>.<stem>`` where ``stem`` matches ``materialize_tiers._stem_from_id``.
"""

from __future__ import annotations

import ast
import keyword
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_STDLIB_TOP = frozenset({
    "abc", "argparse", "array", "ast", "asyncio", "base64", "binascii", "bisect",
    "builtins", "bz2", "calendar", "collections", "contextlib", "copy", "csv",
    "dataclasses", "datetime", "decimal", "enum", "functools", "gc", "hashlib",
    "importlib", "inspect", "io", "itertools", "json", "keyword", "logging",
    "math", "operator", "os", "pathlib", "pickle", "platform", "queue", "random",
    "re", "secrets", "shutil", "signal", "socket", "sqlite3", "string", "struct",
    "subprocess", "sys", "tempfile", "textwrap", "threading", "time", "typing",
    "unicodedata", "urllib", "uuid", "warnings", "weakref", "xml", "zipfile",
})


def _stem_from_id(cid: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._]+", "_", cid.strip())
    return s.replace(".", "_") or "component"


def _norm_path(p: str | Path) -> str:
    try:
        return Path(p).resolve().as_posix()
    except OSError:
        return str(p)


def _safe_resolve_path(p: Path) -> Path:
    """Resolve when possible; keep unresolved path on ``OSError`` (host / test hooks)."""
    try:
        return p.resolve()
    except OSError:
        return p


@dataclass(frozen=True)
class CNAImportTarget:
    tier: str
    stem: str
    component_id: str
    export_name: str

    @property
    def qualified_module(self) -> str:
        return f"{self.tier}.{self.stem}"


def build_cna_import_index(plan: dict[str, Any]) -> dict[tuple[str, str], CNAImportTarget]:
    """Map ``(resolved_source_py_path, symbol_name_lower)`` -> materialized target."""
    out: dict[tuple[str, str], CNAImportTarget] = {}
    for prop in plan.get("proposed_components") or []:
        sym = prop.get("source_symbol") or {}
        path = sym.get("path") or ""
        name = str(sym.get("name") or prop.get("name") or "")
        cid = str(prop.get("id") or "")
        tier = str(prop.get("tier") or "")
        if not path or not name or not cid or not tier:
            continue
        key = (_norm_path(path), name.lower())
        out[key] = CNAImportTarget(
            tier=tier,
            stem=_stem_from_id(cid),
            component_id=cid,
            export_name=name,
        )
    return out


def _candidate_module_files(module: str, root: Path) -> list[Path]:
    """Resolve ``dotted.module`` to plausible ``.py`` paths under ``root``."""
    rel = module.replace(".", "/")
    base = (root / rel).resolve()
    out: list[Path] = []
    py = base.with_suffix(".py")
    if py.is_file():
        out.append(py)
    init_py = base / "__init__.py"
    if init_py.is_file():
        out.append(init_py)
    return out


def resolve_import_from_module(
    module: str,
    name: str,
    *,
    index: dict[tuple[str, str], CNAImportTarget],
    source_roots: list[Path],
) -> CNAImportTarget | None:
    """Resolve ``from module import name`` using CNA index and source roots."""
    top = module.split(".", 1)[0]
    if top in _STDLIB_TOP:
        return None
    for root in source_roots:
        r = Path(root).resolve()
        for cand in _candidate_module_files(module, r):
            key = (cand.as_posix(), name.lower())
            hit = index.get(key)
            if hit is not None:
                return hit
    return None


def _module_paths_absolute(module: str, roots: list[Path]) -> list[Path]:
    out: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        for cand in _candidate_module_files(module, Path(root).resolve()):
            px = cand.resolve().as_posix()
            if px not in seen:
                seen.add(px)
                out.append(cand)
    return out


def _relative_base_dir(owning_py: Path, level: int) -> Path:
    base = owning_py.resolve().parent
    for _ in range(level - 1):
        base = base.parent
    return base


def _paths_for_relative_module(owning_py: Path, level: int, module: str) -> list[Path]:
    base = _relative_base_dir(owning_py, level)
    file_base = base.joinpath(*module.split("."))
    out: list[Path] = []
    py = file_base.with_suffix(".py")
    if py.is_file():
        out.append(py.resolve())
    init_py = file_base / "__init__.py"
    if init_py.is_file():
        out.append(init_py.resolve())
    return out


def _paths_for_import_from(
    module: str | None,
    level: int,
    *,
    owning_py: Path | None,
    source_roots: list[Path],
) -> list[Path]:
    if level and level > 0:
        if not owning_py or not module:
            return []
        return _paths_for_relative_module(owning_py, level, module)
    if not module:
        return []
    return _module_paths_absolute(module, source_roots)


def _targets_for_source_file(
    py_file: Path, index: dict[tuple[str, str], CNAImportTarget]
) -> list[CNAImportTarget]:
    px = py_file.resolve().as_posix()
    by_id: dict[str, CNAImportTarget] = {}
    for (p, _), tgt in index.items():
        if p == px:
            by_id[tgt.component_id] = tgt
    return list(by_id.values())


def resolve_import_from_module_any(
    module: str | None,
    name: str,
    level: int,
    *,
    owning_source: Path | None,
    index: dict[tuple[str, str], CNAImportTarget],
    source_roots: list[Path],
) -> CNAImportTarget | None:
    """Resolve ``from … import name`` for absolute or relative imports."""
    if level and level > 0:
        if not module or not owning_source:
            return None
        top = module.split(".", 1)[0]
        if top in _STDLIB_TOP:
            return None
    elif module:
        top = module.split(".", 1)[0]
        if top in _STDLIB_TOP:
            return None
    else:
        return None
    for cand in _paths_for_import_from(
        module, level, owning_py=owning_source, source_roots=source_roots
    ):
        hit = index.get((cand.resolve().as_posix(), name.lower()))
        if hit is not None:
            return hit
    return None


def _parse_flat_import_ref(ref: str) -> tuple[str, str] | None:
    """Parse strings like ``pkg.mod.Symbol`` -> (``pkg.mod``, ``Symbol``)."""
    ref = ref.strip()
    if not ref or "." not in ref:
        return None
    mod, _, tail = ref.rpartition(".")
    if not mod or not tail:
        return None
    if not tail.isidentifier() or keyword.iskeyword(tail):
        return None
    for part in mod.split("."):
        if not part.isidentifier() or keyword.iskeyword(part):
            return None
    return mod, tail


class _AssimilateImportRewriter(ast.NodeTransformer):
    """Rewrite ``import`` / ``from`` to materialized ``<tier>.<stem>`` (CNA targets)."""

    def __init__(
        self,
        index: dict[tuple[str, str], CNAImportTarget],
        roots: list[Path],
        stats: dict[str, int],
        owning_source: Path | None,
    ) -> None:
        self._index = index
        self._roots = [_safe_resolve_path(Path(r)) for r in roots]
        self._stats = stats
        try:
            self._owning = Path(owning_source).resolve() if owning_source else None
        except OSError:
            self._owning = Path(owning_source) if owning_source else None

    def _plain_import_module_stub(
        self, path: Path, alias: ast.alias, template: ast.AST
    ) -> list[ast.stmt] | None:
        """``import pkg.mod`` / ``from . import mod`` -> ``import <tier>.<stem>`` (single CNA row per file)."""
        tgts = _targets_for_source_file(path, self._index)
        if len(tgts) != 1:
            return None
        tgt = tgts[0]
        q = f"{tgt.tier}.{tgt.stem}"
        if alias.asname:
            bind = alias.asname
        elif "." in alias.name:
            bind = alias.name.rpartition(".")[-1]
        else:
            bind = alias.name
        asnm: str | None = bind if bind != tgt.stem else None
        new_alias = ast.alias(name=q, asname=asnm)
        self._stats.setdefault("import_stmt_rewritten", 0)
        self._stats["import_stmt_rewritten"] += 1
        return [ast.copy_location(ast.Import(names=[new_alias]), template)]

    def visit_Import(self, node: ast.Import) -> ast.AST | list[ast.stmt]:
        out: list[ast.stmt] = []
        pending: list[ast.alias] = []
        rewrote = False

        def flush() -> None:
            nonlocal pending
            if pending:
                out.append(ast.copy_location(ast.Import(names=list(pending)), node))
                pending.clear()

        for alias in node.names:
            top = alias.name.split(".", 1)[0]
            if top in _STDLIB_TOP:
                pending.append(alias)
                continue
            paths = _module_paths_absolute(alias.name, self._roots)
            if not paths:
                pending.append(alias)
                continue
            rep = self._plain_import_module_stub(paths[0], alias, node)
            if rep is None:
                pending.append(alias)
            else:
                flush()
                out.extend(rep)
                rewrote = True
        flush()
        if not rewrote:
            return node
        if len(out) == 1:
            return out[0]
        return out

    def _visit_relative_import_only_submodules(self, node: ast.ImportFrom) -> ast.AST | list[ast.stmt]:
        """``from . import foo`` (submodule) -> ``import <tier>.<stem>`` when unambiguous."""
        level = int(node.level or 0)
        if not self._owning or level <= 0:
            return node
        if any(a.name == "*" for a in node.names):
            return node
        own = self._owning
        out: list[ast.stmt] = []
        pending: list[ast.alias] = []
        rewrote = False

        def flush() -> None:
            nonlocal pending
            if pending:
                out.append(
                    ast.copy_location(
                        ast.ImportFrom(module=None, names=list(pending), level=level),
                        node,
                    )
                )
                pending.clear()

        for alias in node.names:
            base = _relative_base_dir(own, level)
            sub_paths = _candidate_module_files(alias.name, base)
            if not sub_paths:
                pending.append(alias)
                continue
            rep = self._plain_import_module_stub(sub_paths[0], alias, node)
            if rep is None:
                pending.append(alias)
            else:
                flush()
                out.extend(rep)
                rewrote = True
        flush()
        if not rewrote:
            return node
        if len(out) == 1:
            return out[0]
        return out

    def _expand_star(self, node: ast.ImportFrom, paths: list[Path]) -> ast.AST | list[ast.stmt] | None:
        if not paths:
            return None
        px = paths[0].resolve().as_posix()
        groups: dict[tuple[str, str], list[str]] = {}
        for (p, _), tgt in self._index.items():
            if p != px:
                continue
            groups.setdefault((tgt.tier, tgt.stem), []).append(tgt.export_name)
        if not groups:
            return None
        new_nodes: list[ast.stmt] = []
        for (tier, stem), names in sorted(groups.items()):
            uniq = sorted(set(names))
            als = [ast.alias(n) for n in uniq]
            new_nodes.append(
                ast.copy_location(
                    ast.ImportFrom(module=f"{tier}.{stem}", names=als, level=0),
                    node,
                )
            )
        if len(new_nodes) == 1:
            return new_nodes[0]
        return new_nodes

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.AST | list[ast.stmt]:
        level = int(node.level or 0)
        mod = node.module

        if level > 0 and not mod:
            return self._visit_relative_import_only_submodules(node)

        if any(a.name == "*" for a in node.names):
            if level > 0 and not self._owning:
                return node
            paths = _paths_for_import_from(
                mod, level, owning_py=self._owning, source_roots=self._roots
            )
            exp = self._expand_star(node, paths)
            if exp is not None:
                self._stats.setdefault("star_expanded", 0)
                self._stats["star_expanded"] += 1
            return exp if exp is not None else node

        if not mod:
            return node

        groups: dict[tuple[str, str], list[ast.alias]] = {}
        unmapped: list[ast.alias] = []
        for alias in node.names:
            hit = resolve_import_from_module_any(
                mod,
                alias.name,
                level,
                owning_source=self._owning,
                index=self._index,
                source_roots=self._roots,
            )
            if hit is None:
                unmapped.append(alias)
            else:
                groups.setdefault((hit.tier, hit.stem), []).append(alias)
                self._stats["imports_rewritten"] += 1
        if not groups:
            return node
        new_nodes: list[ast.stmt] = []
        for (tier, stem), als in sorted(groups.items()):
            new_nodes.append(
                ast.copy_location(
                    ast.ImportFrom(module=f"{tier}.{stem}", names=als, level=0),
                    node,
                )
            )
        if unmapped:
            rel_mod = mod
            new_nodes.append(
                ast.copy_location(
                    ast.ImportFrom(
                        module=rel_mod, names=unmapped, level=0 if level == 0 else level
                    ),
                    node,
                )
            )
        if len(new_nodes) == 1:
            return new_nodes[0]
        return new_nodes


def rewrite_python_imports_in_body(
    body: str,
    *,
    source_roots: list[Path],
    index: dict[tuple[str, str], CNAImportTarget],
    owning_source_file: str | Path | None = None,
) -> tuple[str, dict[str, int]]:
    """Parse *body* and rewrite third-party (ingested) imports into materialized CNA modules.

    *owning_source_file* enables relative ``from .`` / ``from ..`` resolution against the
    original file path of this component.
    """
    stats: dict[str, int] = {"imports_rewritten": 0}
    owning: Path | None = None
    if owning_source_file:
        try:
            owning = Path(owning_source_file).resolve()
        except OSError:
            owning = Path(str(owning_source_file))
    try:
        tree = ast.parse(body)
    except SyntaxError:
        return body, {"imports_rewritten": 0, "ast_error": 1}
    rw = _AssimilateImportRewriter(index, source_roots, stats, owning)
    new_tree = rw.visit(tree)
    ast.fix_missing_locations(new_tree)
    try:
        out = ast.unparse(new_tree)
    except AttributeError:
        return body, {"imports_rewritten": 0, "no_unparse": 1}
    if out != body:
        stats["body_changed"] = 1
    return out, stats


def build_prepended_import_lines(
    prop: dict[str, Any],
    *,
    owning_source_file: str,
    index: dict[tuple[str, str], CNAImportTarget],
    source_roots: list[Path],
) -> tuple[list[str], dict[str, int]]:
    """Synthesize ``from <tier>.<stem> import …`` for file-level deps (enrich ``imports``)."""
    stats = {"prepended": 0, "unresolved": 0}
    seen: set[tuple[str, str, str]] = set()
    lines: list[str] = []
    _ = owning_source_file  # reserved for future relative-import / same-file filtering

    for raw in prop.get("imports") or []:
        if not isinstance(raw, str):
            continue
        parsed = _parse_flat_import_ref(raw)
        if parsed is None:
            continue
        mod, nm = parsed
        if mod.split(".", 1)[0] in _STDLIB_TOP:
            continue
        hit = resolve_import_from_module(mod, nm, index=index, source_roots=source_roots)
        if hit is None:
            stats["unresolved"] += 1
            continue
        dedupe = (hit.tier, hit.stem, nm)
        if dedupe in seen:
            continue
        seen.add(dedupe)
        lines.append(f"from {hit.qualified_module} import {nm}")
        stats["prepended"] += 1

    return lines, stats


def _dedupe_from_import_lines(text: str) -> str:
    """Drop duplicate import lines (prepend + AST rewrite overlap)."""
    seen: set[str] = set()
    out_lines: list[str] = []
    for line in text.splitlines():
        st = line.strip()
        if (
            st.startswith("from ")
            and " import " in st
            and not st.startswith("from .")
            and not st.startswith("from ..")
        ):
            if st in seen:
                continue
            seen.add(st)
        elif st.startswith("import ") and not st.startswith("import ("):
            if st in seen:
                continue
            seen.add(st)
        out_lines.append(line)
    return "\n".join(out_lines)


def assimilate_component_body(
    body: str,
    prop: dict[str, Any],
    *,
    gap_plan: dict[str, Any],
    source_roots: list[Path],
) -> tuple[str, dict[str, Any]]:
    """Rewrite imports for one materialized component; returns body + receipt.

    CNA index maps ``(resolved .py path, symbol name)`` -> ``<tier>.<stem>`` (materialized
    module). Absolute paths keep collisions impossible across repos when sources differ.
    ``from pkg import a, b`` is split: resolved symbols rewrite to tier modules; unresolved
    names stay on a trailing ``from pkg import …``. Plain ``import pkg.mod`` rewrites when
    exactly one CNA component maps to that module file (binding name preserved via ``as``).
    Relative imports require ``source_symbol.path`` so the rewriter can resolve ``from .`` /
    ``from ..``. ``from m import *`` expands to explicit ``from <tier>.<stem> import …`` for
    symbols present in the gap plan for that source file.
    """
    if not source_roots or not body.strip():
        return body, {"skipped": True}

    index = build_cna_import_index(gap_plan)
    sym = prop.get("source_symbol") or {}
    owning = str(sym.get("path") or "")

    prepend, pstats = build_prepended_import_lines(
        prop, owning_source_file=owning, index=index, source_roots=source_roots
    )
    body2, rstats = rewrite_python_imports_in_body(
        body,
        source_roots=source_roots,
        index=index,
        owning_source_file=owning or None,
    )

    parts: list[str] = []
    if prepend:
        parts.append("\n".join(prepend))
    parts.append(body2.strip("\n"))
    final = "\n\n".join(p for p in parts if p)
    final = _dedupe_from_import_lines(final)
    receipt = {"prepend": pstats, "inline": rstats}
    return final + ("\n" if final and not final.endswith("\n") else ""), receipt
