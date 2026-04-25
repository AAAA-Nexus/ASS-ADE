"""Project Ingestor — scan source files and classify symbols into tiers.

Self-contained: no external registry dependency. Pass an optional
``registry`` list of existing component dicts to enable registry matching.
"""

from __future__ import annotations

import ast
import datetime as dt
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from ass_ade.engine.rebuild.tiers import TIER_PREFIX, TIERS

INGESTION_SCHEMA = "ASSADE-SPEC-005"

SOURCE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".rs"}
EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "engine_out", "target",
    "dist", "build", "rebuilds", "drafts", "__pycache__", ".pytest_cache",
    ".pytest_tmp", ".ruff_cache", ".next", ".turbo", "reports",
    ".ass-ade-pytest-basetemp", ".ass-ade",
    ".atomadic", ".claude", ".cursor", ".github", ".vscode",
    "a0_qk_constants", "a1_at_functions", "a2_mo_composites",
    "a3_og_features", "a4_sy_orchestration",
}
MAX_FILE_BYTES = 750_000

TS_SYMBOL_PATTERNS = [
    re.compile(r"^\s*export\s+function\s+([A-Za-z_$][\w$]*)", re.MULTILINE),
    re.compile(r"^\s*function\s+([A-Za-z_$][\w$]*)", re.MULTILINE),
    re.compile(r"^\s*export\s+const\s+([A-Za-z_$][\w$]*)\s*=", re.MULTILINE),
    re.compile(r"^\s*const\s+([A-Za-z_$][\w$]*)\s*=", re.MULTILINE),
    re.compile(r"^\s*export\s+class\s+([A-Za-z_$][\w$]*)", re.MULTILINE),
    re.compile(r"^\s*class\s+([A-Za-z_$][\w$]*)", re.MULTILINE),
]
RS_SYMBOL_PATTERNS = [
    re.compile(r"^\s*(?:pub\s+)?fn\s+([A-Za-z_][\w]*)", re.MULTILINE),
    re.compile(r"^\s*(?:pub\s+)?struct\s+([A-Za-z_][\w]*)", re.MULTILINE),
    re.compile(r"^\s*(?:pub\s+)?enum\s+([A-Za-z_][\w]*)", re.MULTILINE),
]


@dataclass
class Symbol:
    name: str
    kind: str
    language: str
    path: str
    line: int


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "component"


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def iter_source_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() in SOURCE_SUFFIXES:
                yield path


def _read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _extract_python_symbols(path: Path, text: str) -> list[Symbol]:
    symbols: list[Symbol] = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return symbols
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append(Symbol(node.name, "function", "python", path.as_posix(), node.lineno))
        elif isinstance(node, ast.ClassDef):
            symbols.append(Symbol(node.name, "class", "python", path.as_posix(), node.lineno))
    return symbols


def _extract_regex_symbols(
    path: Path, text: str, language: str, patterns: list[re.Pattern[str]]
) -> list[Symbol]:
    symbols: list[Symbol] = []
    for pattern in patterns:
        for match in pattern.finditer(text):
            name = match.group(1)
            raw = match.group(0)
            kind = "class" if "class" in raw else "function"
            if "struct" in raw or "enum" in raw:
                kind = "type"
            symbols.append(Symbol(name, kind, language, path.as_posix(), _line_number(text, match.start())))
    dedup: dict[tuple[str, int], Symbol] = {}
    for symbol in symbols:
        dedup[(symbol.name, symbol.line)] = symbol
    return list(dedup.values())


def extract_symbols(path: Path) -> list[Symbol]:
    text = _read_text(path)
    if text is None:
        return []
    suffix = path.suffix.lower()
    if suffix == ".py":
        return _extract_python_symbols(path, text)
    if suffix in {".ts", ".tsx", ".js", ".jsx"}:
        return _extract_regex_symbols(path, text, "typescript", TS_SYMBOL_PATTERNS)
    if suffix == ".rs":
        return _extract_regex_symbols(path, text, "rust", RS_SYMBOL_PATTERNS)
    return []


def classify_tier(symbol: Symbol) -> str:
    haystack = f"{symbol.path} {symbol.name} {symbol.kind}".lower()
    if any(term in haystack for term in (
        "constant", "const", "schema", "manifest", "token", "invariant", "proof"
    )):
        return "a0_qk_constants"
    if any(term in haystack for term in (
        "button", "textarea", "input", "validator", "validate", "format", "parse", "atom"
    )):
        return "a1_at_functions"
    if any(term in haystack for term in (
        "engine", "service", "client", "manager", "store", "hook", "calculator", "molecule"
    )):
        return "a2_mo_composites"
    if any(term in haystack for term in (
        "registry", "gateway", "vault", "module", "feature", "workflow", "page", "screen", "organism"
    )):
        return "a3_og_features"
    if any(term in haystack for term in (
        "server", "router", "orchestrator", "bridge", "runtime", "system", "main", "mcp"
    )):
        return "a4_sy_orchestration"
    if symbol.kind == "function":
        return "a1_at_functions"
    if symbol.kind == "class":
        return "a2_mo_composites"
    return "a1_at_functions"


def product_categories(symbol: Symbol) -> list[str]:
    haystack = f"{symbol.path} {symbol.name}".lower()
    categories: list[str] = []
    if any(term in haystack for term in ("pay", "x402", "billing", "fee", "price")):
        categories.append("PAY")
    if any(term in haystack for term in ("identity", "delegation", "trust", "ucan")):
        categories.append("IDT")
    if any(term in haystack for term in ("theorem", "rag", "search", "answer", "proof")):
        categories.append("DCM")
    if any(term in haystack for term in ("audit", "compliance", "policy", "vault")):
        categories.append("SRG")
    if any(term in haystack for term in ("security", "crypto", "pqc", "threat")):
        categories.append("SEC")
    if not categories:
        categories.append("COR")
    return categories


def _registry_match(symbol: Symbol, registry: list[dict[str, Any]]) -> str | None:
    symbol_key = _normalize(symbol.name)
    for component in registry:
        candidates = [
            _normalize(component.get("id", "")),
            _normalize(component.get("name", "")),
            _normalize(Path(component.get("_implementation") or "").stem),
        ]
        if symbol_key in candidates:
            return component["id"]
        if any(symbol_key and symbol_key in c for c in candidates):
            return component["id"]
    return None


def classify_symbol(
    symbol: Symbol,
    root_id: str,
    registry: list[dict[str, Any]],
) -> dict[str, Any]:
    tier = classify_tier(symbol)
    prefix = TIER_PREFIX[tier]
    match = _registry_match(symbol, registry)
    component_id = match or f"{prefix}.source.{_slug(root_id)}.{_slug(symbol.name)}"
    return {
        "source_symbol": asdict(symbol),
        "tier": tier,
        "candidate_id": component_id,
        "registry_match": match,
        "product_categories": product_categories(symbol),
        "status": "mapped" if match else "gap",
    }


def ingest_project(
    source_root: Path,
    root_id: str = "source",
    *,
    registry: list[dict[str, Any]] | None = None,
    emit_drafts: bool = False,
    draft_dir: Path | None = None,
    progress_callback: "Any | None" = None,
) -> dict[str, Any]:
    """Scan ``source_root`` and return an ingestion report dict.

    Args:
        source_root: Directory to scan.
        root_id: Logical identifier for this project root.
        registry: Optional list of existing component specs for registry matching.
        emit_drafts: Write draft JSON files for each gap.
        draft_dir: Where to write draft files (only used when ``emit_drafts`` is True).
        progress_callback: Optional callable(current, total) called per file processed.
    """
    registry = registry or []
    symbols: list[Symbol] = []
    all_files = list(iter_source_files(source_root))
    total_files = len(all_files)
    for idx, path in enumerate(all_files, 1):
        symbols.extend(extract_symbols(path))
        if progress_callback is not None:
            try:
                progress_callback(idx, total_files)
            except Exception:
                pass

    candidates = [classify_symbol(s, root_id, registry) for s in symbols]
    gaps = [c for c in candidates if c["status"] == "gap"]
    draft_paths: list[str] = []
    if emit_drafts and draft_dir is not None:
        draft_paths = _emit_draft_components(gaps, root_id, draft_dir)

    by_tier: dict[str, int] = {}
    for c in candidates:
        tier = c["tier"]
        by_tier[tier] = by_tier.get(tier, 0) + 1

    files_scanned = total_files
    return {
        "ingestion_schema": INGESTION_SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_root": source_root.as_posix(),
        "root_id": root_id,
        "mode": "draft-components" if emit_drafts else "report-only",
        "summary": {
            "files_scanned": files_scanned,
            "symbols": len(symbols),
            "candidate_components": len(candidates),
            "mapped": sum(1 for c in candidates if c["status"] == "mapped"),
            "gaps": len(gaps),
            "drafts_written": len(draft_paths),
            "by_tier": by_tier,
        },
        "symbols": [asdict(s) for s in symbols],
        "candidate_components": candidates,
        "gaps": gaps,
        "draft_paths": draft_paths,
    }


def _emit_draft_components(
    gaps: list[dict[str, Any]], root_id: str, draft_dir: Path
) -> list[str]:
    draft_paths: list[str] = []
    for gap in gaps:
        symbol = gap["source_symbol"]
        tier = gap["tier"]
        prefix = TIER_PREFIX[tier]
        directory = draft_dir / tier
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{prefix}_source_{_slug(root_id)}_{_slug(symbol['name'])}.json"
        payload = {
            "component_schema": "ASSADE-SPEC-003",
            "id": gap["candidate_id"],
            "tier": tier,
            "name": symbol["name"],
            "kind": f"ingested_{symbol['kind']}",
            "description": f"Draft candidate ingested from {symbol['path']}:{symbol['line']}.",
            "made_of": [],
            "provides": [f"source-map candidate for {symbol['name']}"],
            "interfaces": {"source": f"{symbol['path']}:{symbol['line']}"},
            "reuse_policy": "reference-only",
            "status": "draft",
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        draft_paths.append(path.as_posix())
    return draft_paths
