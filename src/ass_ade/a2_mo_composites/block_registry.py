"""Tier a2 — Block Registry.

Walks a monadic source tree and indexes every public symbol (function, class,
constant) as a draggable "block" for the playground. Each block records its
tier, signature, dependencies, test coverage signal, and a stable id.

Used by:
  - /playground/blocks (dashboard palette)
  - composition_engine (resolve block_ids to source segments)
  - atomadic_copilot (knowledge base for brainstorming)
"""

from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.tier_names import TIERS, TIER_PREFIX


_SKIP_DIRS = frozenset({
    ".git", ".hg", ".svn", ".venv", "__pycache__", "node_modules",
    "dist", "build", ".pytest_cache", ".ruff_cache", ".ass-ade",
})


@dataclass
class Block:
    """A single draggable block — a function, class, or constant."""
    id: str                         # stable hash-based id
    name: str                       # symbol name (e.g. "scout_repo")
    qualname: str                   # dotted module path + symbol
    tier: str                       # a0_qk_constants ... a4_sy_orchestration
    tier_prefix: str                # a0 | a1 | a2 | a3 | a4
    kind: str                       # function | class | constant | coroutine
    module: str                     # module dotted path
    file: str                       # file path (relative to source_dir)
    lineno: int
    end_lineno: int
    signature: str = ""             # "(x: int, y: str = 'a') -> bool" or ""
    docstring: str = ""             # first line of docstring
    imports: list[str] = field(default_factory=list)  # top-level modules referenced
    has_test: bool = False          # heuristic: test file with same stem exists
    is_public: bool = True          # not leading-underscore

    def to_dict(self) -> dict:
        return asdict(self)


def _is_skipped(rel_parts: tuple[str, ...]) -> bool:
    return any(part in _SKIP_DIRS for part in rel_parts)


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = node.args
    parts: list[str] = []
    all_pos = list(args.posonlyargs) + list(args.args)
    defaults_offset = len(all_pos) - len(args.defaults)
    for i, arg in enumerate(all_pos):
        suffix = "=" if i >= defaults_offset else ""
        ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
        parts.append(f"{arg.arg}{ann}{suffix}")
    if args.vararg:
        parts.append(f"*{args.vararg.arg}")
    elif args.kwonlyargs:
        parts.append("*")
    for arg, default in zip(args.kwonlyargs, args.kw_defaults, strict=True):
        ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
        eq = "=" if default is not None else ""
        parts.append(f"{arg.arg}{ann}{eq}")
    if args.kwarg:
        parts.append(f"**{args.kwarg.arg}")
    ret = ""
    if node.returns is not None:
        try:
            ret = f" -> {ast.unparse(node.returns)}"
        except Exception:
            ret = ""
    return f"({', '.join(parts)}){ret}"


def _docstring_first_line(node: ast.AST) -> str:
    doc = ast.get_docstring(node) or ""
    return doc.splitlines()[0] if doc else ""


def _module_imports(tree: ast.AST) -> list[str]:
    names: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for alias in n.names:
                names.add(alias.name.split(".", 1)[0])
        elif isinstance(n, ast.ImportFrom) and n.module:
            names.add(n.module.split(".", 1)[0])
    return sorted(names)


def _block_id(qualname: str, body_hash: str) -> str:
    return hashlib.sha1(f"{qualname}:{body_hash}".encode("utf-8")).hexdigest()[:16]


def _body_hash(source: str, node: ast.AST) -> str:
    seg = ast.get_source_segment(source, node) or ast.dump(node)
    return hashlib.sha256(seg.encode("utf-8")).hexdigest()[:16]


def _has_nearby_test(root: Path, file_path: Path) -> bool:
    stem = file_path.stem
    for test_name in (f"test_{stem}.py", f"{stem}_test.py"):
        for tdir in ("tests", "test"):
            if (root / tdir / test_name).is_file():
                return True
            if (root.parent / tdir / test_name).is_file():
                return True
    return False


def _tier_for_path(rel_path: Path) -> str | None:
    for tier in TIERS:
        if rel_path.parts and rel_path.parts[0] == tier:
            return tier
    return None


def _module_dotted(rel_path: Path, source_dir: Path) -> str:
    rel = rel_path.with_suffix("")
    parts = [p for p in rel.parts if p != "__init__"]
    return ".".join(parts)


class BlockRegistry:
    """In-memory registry of every public symbol in a monadic source tree."""

    def __init__(self, source_dir: Path) -> None:
        self._source_dir = source_dir.resolve()
        self._blocks: dict[str, Block] = {}
        self._by_tier: dict[str, list[str]] = {t: [] for t in TIERS}

    @property
    def source_dir(self) -> Path:
        return self._source_dir

    # ── Indexing ───────────────────────────────────────────────────────────

    def scan(self) -> int:
        """Walk source_dir, populate registry. Returns block count."""
        self._blocks.clear()
        for tier_list in self._by_tier.values():
            tier_list.clear()

        for py_file in sorted(self._source_dir.rglob("*.py")):
            rel = py_file.relative_to(self._source_dir)
            if _is_skipped(rel.parts):
                continue
            tier = _tier_for_path(rel)
            if tier is None:
                continue
            try:
                source = py_file.read_text(encoding="utf-8")
                tree = ast.parse(source)
            except (OSError, SyntaxError):
                continue

            module = _module_dotted(rel, self._source_dir)
            imports = _module_imports(tree)
            has_test = _has_nearby_test(self._source_dir, py_file)

            for node in tree.body:
                block = self._block_from_node(
                    node, source, module, tier, rel, imports, has_test
                )
                if block is not None:
                    self._blocks[block.id] = block
                    self._by_tier[tier].append(block.id)

        return len(self._blocks)

    def _block_from_node(
        self,
        node: ast.AST,
        source: str,
        module: str,
        tier: str,
        rel_path: Path,
        module_imports: list[str],
        has_test: bool,
    ) -> Block | None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = "coroutine" if isinstance(node, ast.AsyncFunctionDef) else "function"
            name = node.name
            if name.startswith("_") and not name.startswith("__"):
                return None
            qualname = f"{module}.{name}"
            body = _body_hash(source, node)
            return Block(
                id=_block_id(qualname, body),
                name=name,
                qualname=qualname,
                tier=tier,
                tier_prefix=TIER_PREFIX.get(tier, "?"),
                kind=kind,
                module=module,
                file=str(rel_path).replace("\\", "/"),
                lineno=node.lineno,
                end_lineno=node.end_lineno or node.lineno,
                signature=_signature(node),
                docstring=_docstring_first_line(node),
                imports=module_imports,
                has_test=has_test,
                is_public=not name.startswith("_"),
            )
        if isinstance(node, ast.ClassDef):
            name = node.name
            if name.startswith("_"):
                return None
            qualname = f"{module}.{name}"
            body = _body_hash(source, node)
            return Block(
                id=_block_id(qualname, body),
                name=name,
                qualname=qualname,
                tier=tier,
                tier_prefix=TIER_PREFIX.get(tier, "?"),
                kind="class",
                module=module,
                file=str(rel_path).replace("\\", "/"),
                lineno=node.lineno,
                end_lineno=node.end_lineno or node.lineno,
                signature=f"class {name}",
                docstring=_docstring_first_line(node),
                imports=module_imports,
                has_test=has_test,
                is_public=True,
            )
        if isinstance(node, ast.Assign):
            # Only top-level UPPER_CASE constants
            targets = [t for t in node.targets if isinstance(t, ast.Name)]
            if len(targets) != 1:
                return None
            name = targets[0].id
            if not name.isupper() or name.startswith("_"):
                return None
            qualname = f"{module}.{name}"
            seg = ast.get_source_segment(source, node) or name
            body = hashlib.sha256(seg.encode("utf-8")).hexdigest()[:16]
            return Block(
                id=_block_id(qualname, body),
                name=name,
                qualname=qualname,
                tier=tier,
                tier_prefix=TIER_PREFIX.get(tier, "?"),
                kind="constant",
                module=module,
                file=str(rel_path).replace("\\", "/"),
                lineno=node.lineno,
                end_lineno=node.end_lineno or node.lineno,
                signature="",
                docstring="",
                imports=module_imports,
                has_test=has_test,
                is_public=True,
            )
        return None

    # ── Queries ────────────────────────────────────────────────────────────

    def get(self, block_id: str) -> Block | None:
        return self._blocks.get(block_id)

    def all_blocks(self) -> list[Block]:
        return list(self._blocks.values())

    def by_tier(self, tier: str) -> list[Block]:
        ids = self._by_tier.get(tier, [])
        return [self._blocks[i] for i in ids if i in self._blocks]

    def search(
        self,
        *,
        query: str | None = None,
        tier: str | None = None,
        kind: str | None = None,
        has_test: bool | None = None,
        limit: int = 200,
    ) -> list[Block]:
        """Filter blocks by keyword / tier / kind / test coverage."""
        blocks = self.all_blocks()
        if tier:
            blocks = [b for b in blocks if b.tier == tier or b.tier_prefix == tier]
        if kind:
            blocks = [b for b in blocks if b.kind == kind]
        if has_test is not None:
            blocks = [b for b in blocks if b.has_test == has_test]
        if query:
            q = query.lower()
            blocks = [
                b for b in blocks
                if q in b.name.lower()
                or q in b.qualname.lower()
                or q in b.docstring.lower()
            ]
        blocks.sort(key=lambda b: (b.tier, b.name))
        return blocks[:limit]

    def stats(self) -> dict[str, Any]:
        by_tier: dict[str, int] = {}
        by_kind: dict[str, int] = {}
        tested = 0
        for b in self._blocks.values():
            by_tier[b.tier] = by_tier.get(b.tier, 0) + 1
            by_kind[b.kind] = by_kind.get(b.kind, 0) + 1
            if b.has_test:
                tested += 1
        return {
            "total_blocks": len(self._blocks),
            "by_tier": by_tier,
            "by_kind": by_kind,
            "tested_blocks": tested,
            "source_dir": str(self._source_dir),
        }

    def to_json(self) -> str:
        return json.dumps(
            {"stats": self.stats(), "blocks": [b.to_dict() for b in self.all_blocks()]},
            indent=2,
        )
