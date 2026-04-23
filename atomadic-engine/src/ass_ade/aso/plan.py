"""a3-style ASO planning envelopes — structured dicts only (no network I/O)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.aso.constants import ASO_ENGINE_IDS, MCP_MANIFEST_SOFT_TOKEN_BUDGET


def plan_context_optimization(repo: Path) -> dict[str, Any]:
    return {
        "engine": "COE",
        "objective": "Reduce MCP tool-schema surface area without breaking contracts.",
        "steps": [
            "Inventory ``mcp/server.json`` + ``~/.cursor/mcp.json`` tool counts and serialized size.",
            f"Flag servers whose manifest JSON exceeds ~{MCP_MANIFEST_SOFT_TOKEN_BUDGET} tokens **after** local measurement (do not claim ratios without benchmarks).",
            "Design ``get_tool_schema`` / ``invoke_tool`` shim (mcp-compressor-class) behind a feature flag.",
            "Record before/after token + latency in ``.ass-ade/aso/logs/context-<ts>.json``.",
        ],
        "defer": [
            "Rootless ``execute_script`` sandbox is a separate threat-model + CI harness — not implied here.",
        ],
    }


def plan_swarm_intelligence(repo: Path) -> dict[str, Any]:
    return {
        "engine": "SIE",
        "objective": "Improve swarm coordination and shared durable context.",
        "steps": [
            "Read / write ``.ass-ade/swarm/config.json`` (topology + optional memory endpoint).",
            "Prefer existing Atomadic skills (``uep-swarm-advanced``, ``recon-codebase``) for topology picks.",
            "If adding memX-class service: container image, auth, schema — ship behind explicit env + rollback.",
        ],
        "defer": [
            "AdaptOrch / SAMEP names are integration targets — cite design docs before production claims.",
        ],
    }


def plan_codebase_cortex(repo: Path) -> dict[str, Any]:
    return {
        "engine": "CCE",
        "objective": "Relation-first codebase graph + index hygiene.",
        "steps": [
            "Run tier-safe recon (``map_terrain`` / ``phase0_recon``) scoped to repo root.",
            "Emit graph artifacts under ``.ass-ade/graph/`` using ``.ass-ade/aso/knowledge_graph.schema.json``.",
            "Refresh ``.cursorignore`` from ``templates/ass-ade.cursorignore`` + measured noisy dirs.",
        ],
        "defer": [
            "Neo4j / LanceDB / DeepWiki-class hosts require infra tickets — keep local JSON/ SQLite MVP first.",
        ],
    }


def plan_telemetry_evolution(repo: Path) -> dict[str, Any]:
    return {
        "engine": "TEE",
        "objective": "Observable swarm + MCP behavior with human-gated auto-fixes.",
        "steps": [
            "Define OTel resource attributes + span names in ``.ass-ade/aso/telemetry_metrics.schema.json``.",
            "Export counters/histograms for MCP ``tools/call`` latency and token estimates where instrumented.",
            "Route regressions to ``/epiphany`` + ``@evolutionary-manager`` with rollback + tests.",
        ],
        "defer": [
            "AgentOps / Phoenix dashboards — wire after collector is running in CI or local compose.",
        ],
    }


def plan_full_aso(repo: Path) -> dict[str, Any]:
    return {
        "schema": "ass-ade.aso.full-plan.v0",
        "engines": list(ASO_ENGINE_IDS),
        "lanes": {
            "COE": plan_context_optimization(repo),
            "SIE": plan_swarm_intelligence(repo),
            "CCE": plan_codebase_cortex(repo),
            "TEE": plan_telemetry_evolution(repo),
        },
    }
