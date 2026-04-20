"""Tier a3_og — multi-hop context pack builder with three research lanes."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


_SCHEMA = "atomadic.context-pack.v1"


def _lane_local_recon(target: Path) -> dict[str, Any]:
    files = [str(p) for p in target.rglob("*.py") if not str(p).startswith(".")][:50]
    return {"lane": "local_recon", "files_sampled": len(files), "sample": files[:10]}


def _lane_web_multihop(query: str) -> dict[str, Any]:
    # Placeholder: real impl would call AAAA-Nexus nexus_web_search with multi-hop expansion
    # and mandatory AI-breakthrough scan via nexus_research_radar
    return {
        "lane": "web_multihop",
        "query": query,
        "hops": 0,
        "breakthrough_scan": "skipped - offline mode",
        "results": [],
    }


def _lane_tech_docs(topics: list[str]) -> dict[str, Any]:
    return {"lane": "tech_docs", "topics": topics, "docs_fetched": 0, "results": []}


def build_context_pack(
    target: Path,
    query: str,
    topics: list[str] | None = None,
    out: Path | None = None,
) -> dict[str, Any]:
    """Build a context-pack.json from three lanes and return the pack dict."""
    pack: dict[str, Any] = {
        "schema": _SCHEMA,
        "query": query,
        "target": str(target),
        "lanes": [
            _lane_local_recon(target),
            _lane_web_multihop(query),
            _lane_tech_docs(topics or []),
        ],
    }
    if out is not None:
        out.write_text(json.dumps(pack, indent=2))
    return pack
