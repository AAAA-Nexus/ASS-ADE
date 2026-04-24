"""Tier a1 — pure import violation scanner for monadic source trees.

Detects upward (tier-A importing from tier-B where rank(B) > rank(A)) import
violations in Python files organised under a0–a4 tier directories.  Also
builds a symbol index so callers can propose corrected import paths.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


TIER_RANK: dict[str, int] = {
    "a0_qk_constants": 0,
    "a1_at_functions": 1,
    "a2_mo_composites": 2,
    "a3_og_features": 3,
    "a4_sy_orchestration": 4,
}

_TIER_DIRS: frozenset[str] = frozenset(TIER_RANK)


@dataclass(frozen=True)
class ImportViolation:
    file: str
    file_tier: str
    file_tier_rank: int
    import_stmt: str
    import_lineno: int
    import_end_lineno: int
    imported_module: str
    imported_tier: str
    imported_tier_rank: int
    reason: str


@dataclass(frozen=True)
class SymbolLocation:
    tier: str
    tier_rank: int
    module_path: str
    module_dotted: str


def detect_file_tier(py_file: Path) -> str | None:
    """Return the tier directory name that contains py_file, or None."""
    for part in py_file.parts:
        if part in _TIER_DIRS:
            return part
    return None


def _module_tier(module: str) -> str | None:
    """Extract the first tier directory name from a dotted module path."""
    for part in module.split("."):
        if part in _TIER_DIRS:
            return part
    return None


def _node_to_import_str(node: ast.Import | ast.ImportFrom) -> str:
    """Reconstruct a compact import statement string from an AST node."""
    if isinstance(node, ast.Import):
        names = ", ".join(
            f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
        )
        return f"import {names}"
    level = "." * (node.level or 0)
    mod = node.module or ""
    names = ", ".join(
        f"{a.name} as {a.asname}" if a.asname else a.name for a in node.names
    )
    return f"from {level}{mod} import {names}"


def _violations_in_file(py_file: Path, file_tier: str) -> list[ImportViolation]:
    file_rank = TIER_RANK[file_tier]
    try:
        source = py_file.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(py_file))
    except (SyntaxError, OSError):
        return []

    violations: list[ImportViolation] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        end_lineno: int = getattr(node, "end_lineno", node.lineno)

        if isinstance(node, ast.Import):
            for alias in node.names:
                imp_tier = _module_tier(alias.name)
                if imp_tier and TIER_RANK.get(imp_tier, -1) > file_rank:
                    violations.append(ImportViolation(
                        file=str(py_file),
                        file_tier=file_tier,
                        file_tier_rank=file_rank,
                        import_stmt=_node_to_import_str(node),
                        import_lineno=node.lineno,
                        import_end_lineno=end_lineno,
                        imported_module=alias.name,
                        imported_tier=imp_tier,
                        imported_tier_rank=TIER_RANK[imp_tier],
                        reason=(
                            f"{file_tier!r} (rank {file_rank}) imports from "
                            f"{imp_tier!r} (rank {TIER_RANK[imp_tier]}); "
                            "upward dependency forbidden."
                        ),
                    ))

        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue  # relative imports are intra-package — skip
            mod = node.module or ""
            imp_tier = _module_tier(mod)
            if imp_tier and TIER_RANK.get(imp_tier, -1) > file_rank:
                violations.append(ImportViolation(
                    file=str(py_file),
                    file_tier=file_tier,
                    file_tier_rank=file_rank,
                    import_stmt=_node_to_import_str(node),
                    import_lineno=node.lineno,
                    import_end_lineno=end_lineno,
                    imported_module=mod,
                    imported_tier=imp_tier,
                    imported_tier_rank=TIER_RANK[imp_tier],
                    reason=(
                        f"{file_tier!r} (rank {file_rank}) imports from "
                        f"{imp_tier!r} (rank {TIER_RANK[imp_tier]}); "
                        "upward dependency forbidden."
                    ),
                ))

    return violations


def scan_source_for_violations(source_dir: Path) -> list[ImportViolation]:
    """Walk source_dir and return all upward tier import violations."""
    violations: list[ImportViolation] = []
    for py_file in sorted(source_dir.rglob("*.py")):
        tier = detect_file_tier(py_file)
        if tier is None:
            continue
        violations.extend(_violations_in_file(py_file, tier))
    return violations


def build_symbol_index(
    source_dir: Path,
    *,
    package_prefix: str | None = None,
) -> dict[str, list[SymbolLocation]]:
    """Map exported symbol name -> SymbolLocation list for all tier files.

    package_prefix is prepended to module_dotted paths (e.g. 'ass_ade_v11')
    so that generated import statements use fully qualified module names.
    """
    index: dict[str, list[SymbolLocation]] = {}
    for py_file in sorted(source_dir.rglob("*.py")):
        tier = detect_file_tier(py_file)
        if tier is None:
            continue
        tier_rank = TIER_RANK[tier]
        try:
            source = py_file.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(source, filename=str(py_file))
        except (SyntaxError, OSError):
            continue
        try:
            rel = py_file.relative_to(source_dir)
        except ValueError:
            continue
        parts = list(rel.with_suffix("").parts)
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        dotted = ".".join(parts)
        if package_prefix:
            dotted = f"{package_prefix}.{dotted}"
        loc = SymbolLocation(
            tier=tier,
            tier_rank=tier_rank,
            module_path=str(py_file),
            module_dotted=dotted,
        )
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                index.setdefault(node.name, []).append(loc)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        index.setdefault(target.id, []).append(loc)
    return index


def resolve_correct_import(
    violation: ImportViolation,
    symbol_index: dict[str, list[SymbolLocation]],
) -> str | None:
    """Return a corrected import statement for violation, or None if not auto-fixable.

    Auto-fixable means: every imported symbol has a definition in a module at or
    below the file's tier rank, and all such symbols share at least one common
    module (so a single import statement suffices).
    """
    stmt = violation.import_stmt
    if " import " not in stmt:
        return None

    _, names_part = stmt.split(" import ", 1)
    raw_names = [n.strip() for n in names_part.split(",")]
    symbols = [n.split(" as ")[0].strip() for n in raw_names]
    alias_map: dict[str, str] = {}
    for raw in raw_names:
        if " as " in raw:
            sym, al = raw.split(" as ", 1)
            alias_map[sym.strip()] = al.strip()

    file_rank = violation.file_tier_rank

    # Find candidate module paths that contain ALL requested symbols at ≤ file_rank
    candidate_paths: set[str] | None = None
    for sym in symbols:
        lower_locs = [
            loc for loc in symbol_index.get(sym, [])
            if loc.tier_rank <= file_rank
        ]
        if not lower_locs:
            return None
        paths = {loc.module_path for loc in lower_locs}
        if candidate_paths is None:
            candidate_paths = paths
        else:
            candidate_paths &= paths
        if not candidate_paths:
            return None

    if not candidate_paths:
        return None

    # Pick the lowest-ranked (closest to the file's tier) candidate
    path_to_loc: dict[str, SymbolLocation] = {}
    for locs in symbol_index.values():
        for loc in locs:
            if loc.module_path in candidate_paths:
                existing = path_to_loc.get(loc.module_path)
                if existing is None or loc.tier_rank < existing.tier_rank:
                    path_to_loc[loc.module_path] = loc

    if not path_to_loc:
        return None

    best = min(path_to_loc.values(), key=lambda loc: loc.tier_rank)
    names_str = ", ".join(
        f"{sym} as {alias_map[sym]}" if sym in alias_map else sym
        for sym in symbols
    )
    return f"from {best.module_dotted} import {names_str}"
