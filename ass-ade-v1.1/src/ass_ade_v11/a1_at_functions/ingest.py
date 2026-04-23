"""Project ingestor — scan Python sources and classify symbols into tiers."""

from __future__ import annotations

import ast
import datetime as dt
import fnmatch
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from ass_ade_v11.a0_qk_constants.exclude_dirs import EXCLUDED_DIRS, MAX_FILE_BYTES, SOURCE_SUFFIXES
from ass_ade_v11.a0_qk_constants.policy_types import RootPolicy
from ass_ade_v11.a0_qk_constants.schemas import INGESTION_SCHEMA
from ass_ade_v11.a0_qk_constants.tier_names import TIER_PREFIX
from ass_ade_v11.a1_at_functions.registry_fingerprint import (
    match_registry_row,
    registry_snapshot_ledger,
)


def _matches_any(posix_rel: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatch(posix_rel, pat) for pat in patterns)


@dataclass
class Symbol:
    name: str
    kind: str
    language: str
    path: str
    line: int


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "component"


def iter_source_files(
    root: Path,
    *,
    forbid_globs: tuple[str, ...] = (),
    allow_globs: tuple[str, ...] | None = None,
) -> Iterable[Path]:
    """Yield Python source files under ``root`` honoring policy glob rules.

    ``forbid_globs`` and ``allow_globs`` match the file's **POSIX path relative to
    ``root``**. When ``allow_globs`` is None every non-forbidden file passes.
    """
    root_resolved = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root_resolved):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            try:
                rel = path.resolve().relative_to(root_resolved).as_posix()
            except ValueError:
                rel = path.name
            if forbid_globs and _matches_any(rel, forbid_globs):
                continue
            if allow_globs is not None and not _matches_any(rel, allow_globs):
                continue
            yield path


def _read_text(path: Path, *, max_file_bytes: int | None = None) -> str | None:
    limit = MAX_FILE_BYTES if max_file_bytes is None else max_file_bytes
    try:
        if path.stat().st_size > limit:
            return None
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


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


def extract_symbols(path: Path, *, max_file_bytes: int | None = None) -> list[Symbol]:
    text = _read_text(path, max_file_bytes=max_file_bytes)
    if text is None:
        return []
    if path.suffix.lower() == ".py":
        return _extract_python_symbols(path, text)
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


def classify_symbol(
    symbol: Symbol,
    root_id: str,
    registry: list[dict[str, Any]],
) -> dict[str, Any]:
    tier = classify_tier(symbol)
    prefix = TIER_PREFIX[tier]
    match = match_registry_row(symbol.name, registry)
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
    progress_callback: Any | None = None,
    policy: RootPolicy | None = None,
) -> dict[str, Any]:
    """Scan ``source_root`` and return an ingestion report dict.

    When ``policy`` is provided, ``forbid_globs`` / ``allow_globs`` / ``max_file_bytes``
    constrain which files are walked and read.
    """
    if emit_drafts:
        raise ValueError(
            "emit_drafts is not supported in ass-ade-v1.1 yet; use ingest report-only mode."
        )
    registry = registry or []
    forbid_globs: tuple[str, ...] = tuple(policy["forbid_globs"]) if policy and "forbid_globs" in policy else ()
    allow_globs: tuple[str, ...] | None = (
        tuple(policy["allow_globs"])
        if policy and policy.get("allow_globs") is not None
        else None
    )
    max_file_bytes: int | None = policy["max_file_bytes"] if policy and "max_file_bytes" in policy else None

    symbols: list[Symbol] = []
    all_files = list(
        iter_source_files(source_root, forbid_globs=forbid_globs, allow_globs=allow_globs)
    )
    total_files = len(all_files)
    for idx, path in enumerate(all_files, 1):
        symbols.extend(extract_symbols(path, max_file_bytes=max_file_bytes))
        if progress_callback is not None:
            try:
                progress_callback(idx, total_files)
            except Exception:
                pass

    candidates = [classify_symbol(s, root_id, registry) for s in symbols]
    gaps = [c for c in candidates if c["status"] == "gap"]

    by_tier: dict[str, int] = {}
    for c in candidates:
        tier = c["tier"]
        by_tier[tier] = by_tier.get(tier, 0) + 1

    snap = registry_snapshot_ledger(registry) if registry else None
    policy_applied: dict[str, Any] | None = None
    if policy is not None:
        policy_applied = {
            "role": policy.get("role"),
            "license_class": policy.get("license_class"),
            "forbid_globs": list(forbid_globs),
            "allow_globs": list(allow_globs) if allow_globs is not None else None,
            "max_file_bytes": max_file_bytes,
        }
    return {
        "ingestion_schema": INGESTION_SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_root": source_root.resolve().as_posix(),
        "root_id": root_id,
        "mode": "report-only",
        "registry_snapshot": snap,
        "policy_applied": policy_applied,
        "summary": {
            "files_scanned": total_files,
            "symbols": len(symbols),
            "candidate_components": len(candidates),
            "mapped": sum(1 for c in candidates if c["status"] == "mapped"),
            "gaps": len(gaps),
            "drafts_written": 0,
            "by_tier": by_tier,
        },
        "symbols": [asdict(s) for s in symbols],
        "candidate_components": candidates,
        "gaps": gaps,
        "draft_paths": [],
    }
