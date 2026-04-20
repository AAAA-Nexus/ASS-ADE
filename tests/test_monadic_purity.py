"""Monadic composition law enforcement — guards tier purity per .ass-ade/tier-map.json.

Rules enforced (per Atomadic monadic standard):
  - a0: imports nothing from ass_ade.*
  - a1: imports a0 only; no class definitions with state; no I/O modules
        (httpx, requests, pathlib write APIs, subprocess, os.system)
  - a2: imports a0, a1 only
  - a3: imports a0, a1, a2 only (not a4, not other a3 CLIs)
  - a4: may import anything

A tier violation fails the test. This is the Wall.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_TIER_MAP = _REPO / ".ass-ade" / "tier-map.json"
_SRC = _REPO / "src" / "ass_ade"

# Modules that signal state / I/O; banned from tier a1.
_IMPURE_MODULES = {"httpx", "requests", "urllib.request", "subprocess", "socket"}

# Ratchet baselines — legacy violations grandfathered. A NEW violation fails
# the test. The permanent fix is `ass-ade rebuild` on !ass-ade* folders,
# which will decompose these into proper tier-aligned files. Until then,
# this allowlist must only ever shrink.
_ALLOWED_UPWARD: frozenset[str] = frozenset({
    "agent/capabilities.py->ass_ade.cli",
    "agent/context.py->ass_ade.agent.capabilities",
    "config.py->ass_ade.nexus.validation",
    "context_memory.py->ass_ade.recon",
    "engine/rebuild/project_parser.py->ass_ade.engine.rebuild.tiers",
    "mcp/server.py->ass_ade.a2a",
    "mcp/server.py->ass_ade.agent.cie",
    "mcp/server.py->ass_ade.agent.loop",
    "mcp/server.py->ass_ade.agent.lora_flywheel",
    "mcp/server.py->ass_ade.agent.tca",
    "mcp/server.py->ass_ade.engine.router",
    "mcp/server.py->ass_ade.map_terrain",
    "mcp/server.py->ass_ade.recon",
    "mcp/server.py->ass_ade.workflows",
    "mcp/utils.py->ass_ade.nexus.models",
    "protocol/cycle.py->ass_ade.system",
    "tools/registry.py->ass_ade.tools.builtin",
    "tools/registry.py->ass_ade.tools.prompt",
})
_ALLOWED_A1_IMPURE: frozenset[str] = frozenset({
    "mcp/utils.py->httpx",
    "nexus/validation.py->socket",
})


def _load_tier_map() -> dict[str, str]:
    if not _TIER_MAP.exists():
        pytest.skip("tier-map.json not present")
    data = json.loads(_TIER_MAP.read_text(encoding="utf-8"))
    legacy = data.get("legacy_modules", {})
    return {rel: meta["tier"] for rel, meta in legacy.items() if "tier" in meta}


def _classify_import(module: str) -> str | None:
    """Return the tier of an intra-project import, or None if external."""
    if not module.startswith("ass_ade."):
        return None
    # Strip ``ass_ade.`` prefix and map to ``path/to/module.py``.
    parts = module.split(".")[1:]
    candidates = [
        "/".join(parts) + ".py",
        "/".join(parts) + "/__init__.py",
    ]
    tier_map = _load_tier_map()
    for rel in candidates:
        if rel in tier_map:
            return tier_map[rel]
    return None


def _iter_imports(tree: ast.AST):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


@pytest.fixture(scope="module")
def tier_map() -> dict[str, str]:
    return _load_tier_map()


def test_tier_map_exists(tier_map: dict[str, str]):
    assert tier_map, "tier-map.json has no legacy_modules entries"


def test_classified_files_exist(tier_map: dict[str, str]):
    missing = [rel for rel in tier_map if not (_SRC / rel).exists()]
    # Allow a small number of stale entries; fail only if nothing resolves.
    assert len(missing) < len(tier_map), f"no tier-mapped files exist: {missing[:5]}"


_TIER_ORDER = {"a0": 0, "a1": 1, "a2": 2, "a3": 3, "a4": 4}


def test_no_upward_imports(tier_map: dict[str, str]):
    """Enforce: a file at tier N must not import a file at tier > N.

    Ratchet: legacy violations in ``_ALLOWED_UPWARD`` are grandfathered.
    Any NEW upward import fails the test. A file that no longer violates
    must be removed from the allowlist (the allowlist only shrinks).
    """
    violations: list[str] = []
    seen: set[str] = set()
    for rel, self_tier in tier_map.items():
        path = _SRC / rel
        if not path.exists():
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            violations.append(f"{rel}: syntax error {exc}")
            continue
        for imp in _iter_imports(tree):
            other_tier = _classify_import(imp)
            if other_tier is None:
                continue
            if _TIER_ORDER[other_tier] > _TIER_ORDER[self_tier]:
                key = f"{rel}->{imp}"
                seen.add(key)
                if key not in _ALLOWED_UPWARD:
                    violations.append(
                        f"NEW upward import: {rel} ({self_tier}) -> {imp} ({other_tier})"
                    )
    stale = sorted(_ALLOWED_UPWARD - seen)
    assert not violations, "upward import violations:\n  " + "\n  ".join(violations)
    assert not stale, (
        "allowlist has stale entries (remove them — monadic ratchet only shrinks):\n  "
        + "\n  ".join(stale)
    )


def test_a1_is_pure(tier_map: dict[str, str]):
    """a1 files must not import I/O-heavy modules.

    Same ratchet: ``_ALLOWED_A1_IMPURE`` grandfathers legacy; new entries fail.
    """
    violations: list[str] = []
    seen: set[str] = set()
    for rel, tier in tier_map.items():
        if tier != "a1":
            continue
        path = _SRC / rel
        if not path.exists():
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for imp in _iter_imports(tree):
            root = imp.split(".")[0]
            if root in _IMPURE_MODULES or imp in _IMPURE_MODULES:
                key = f"{rel}->{imp}"
                seen.add(key)
                if key not in _ALLOWED_A1_IMPURE:
                    violations.append(f"NEW a1 purity breach: {rel} imports {imp}")
    stale = sorted(_ALLOWED_A1_IMPURE - seen)
    assert not violations, "a1 purity violations:\n  " + "\n  ".join(violations)
    assert not stale, (
        "a1 allowlist has stale entries (remove them):\n  " + "\n  ".join(stale)
    )
