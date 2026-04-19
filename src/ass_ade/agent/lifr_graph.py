"""v18 pillar 85 — LIFR cumulative verification knowledge graph."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ass_ade.context_memory import (
    VectorMemoryMatch,
    query_vector_memory,
    store_vector_memory,
)


@dataclass
class Match:
    id: str
    score: float
    spec: str
    code: str
    proof: str
    metadata: dict[str, Any]


class LIFRGraph:
    def __init__(self, config: dict, nexus: Any | None = None):
        self._config = config
        self._nexus = nexus
        lifr_cfg = config.get("lifr") or {}
        self._namespace = lifr_cfg.get("namespace", "lifr")
        self._threshold = float(lifr_cfg.get("similarity_threshold", 0.85))
        self._working_dir = config.get("working_dir", ".")
        self._writes = 0
        self._queries = 0

    def store(self, spec: str, code: str, proof: str, metadata: dict | None = None) -> str:
        payload = {
            "spec": spec,
            "code": code,
            "proof": proof,
            "metadata": metadata or {},
        }
        meta = dict(metadata or {})
        meta["tier"] = "lifr"
        meta["payload"] = payload
        result = store_vector_memory(
            text=spec,
            namespace=self._namespace,
            metadata=meta,
            working_dir=self._working_dir,
        )
        self._writes += 1
        return result.id

    def query(self, spec_text: str, top_k: int = 5) -> list[Match]:
        self._queries += 1
        result = query_vector_memory(
            query=spec_text,
            namespace=self._namespace,
            top_k=top_k,
            working_dir=self._working_dir,
        )
        matches: list[Match] = []
        for m in result.matches:
            if m.score < self._threshold:
                continue
            payload = (m.metadata or {}).get("payload") or {}
            matches.append(
                Match(
                    id=m.id,
                    score=m.score,
                    spec=payload.get("spec", m.text),
                    code=payload.get("code", ""),
                    proof=payload.get("proof", ""),
                    metadata=m.metadata or {},
                )
            )
        return matches

    def run(self, ctx: dict) -> dict:
        op = ctx.get("op", "query")
        if op == "store":
            mid = self.store(
                ctx.get("spec", ""),
                ctx.get("code", ""),
                ctx.get("proof", ""),
                ctx.get("metadata"),
            )
            return {"id": mid, "stored": True}
        matches = self.query(ctx.get("spec", ""), int(ctx.get("top_k", 5)))
        return {"matches": [m.__dict__ for m in matches]}

    def report(self) -> dict:
        return {
            "engine": "lifr_graph",
            "namespace": self._namespace,
            "threshold": self._threshold,
            "writes": self._writes,
            "queries": self._queries,
        }
