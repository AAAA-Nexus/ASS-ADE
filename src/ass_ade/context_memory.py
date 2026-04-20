"""Phase 0 context tools and local vector memory.

This is the public-safe, local substrate for ASS-ADE context recall. It uses a
small deterministic hashing vector so the free shell has useful recall without
exposing private retrieval internals.

**Trust-scored retrieval:** ``query_vector_memory`` can drop weak matches with
``min_score`` (cosine = dot product on L2-normalized hashing vectors). When
``min_score`` is omitted, ``ASS_ADE_MEMORY_MIN_SCORE`` (optional env) is applied;
if unset, no floor is used (``0.0``). Thresholds are **repo-owned** — tune for
your embedding backend; hashing vectors rarely justify aggressive floors like 0.85.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from ass_ade.recon import phase0_recon

VECTOR_DIMENSIONS = 256
MEMORY_DIR = ".ass-ade/vector-memory"
MEMORY_FILE = "vectors.jsonl"
# Optional default floor for retrieval (float). Unset or empty = no env floor.
_ENV_MIN_SCORE = "ASS_ADE_MEMORY_MIN_SCORE"

_TOKEN_RE = re.compile(r"[a-zA-Z0-9_]{2,}")


class ContextFile(BaseModel):
    path: str
    sha256: str
    size_bytes: int
    excerpt: str
    truncated: bool = False


class ContextPacket(BaseModel):
    task_description: str
    recon_verdict: str
    source_urls: list[str] = Field(default_factory=list)
    files: list[ContextFile] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class VectorMemoryRecord(BaseModel):
    id: str
    namespace: str
    text: str
    vector: list[float]
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str


class VectorMemoryStoreResult(BaseModel):
    id: str
    namespace: str
    path: str


class VectorMemoryMatch(BaseModel):
    id: str
    namespace: str
    score: float
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str


class VectorMemoryQueryResult(BaseModel):
    query: str
    namespace: str
    matches: list[VectorMemoryMatch] = Field(default_factory=list)
    min_score_applied: float = 0.0
    below_threshold_omitted: int = 0


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def vector_embed(text: str, dimensions: int = VECTOR_DIMENSIONS) -> list[float]:
    """Embed text into a deterministic signed hashing vector."""
    if dimensions <= 0:
        raise ValueError("dimensions must be positive")

    vector = [0.0] * dimensions
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        weight = 1.0 + (len(token) % 7) / 10.0
        vector[index] += sign * weight

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def _memory_path(working_dir: str | Path) -> Path:
    root = Path(working_dir).resolve()
    return root / MEMORY_DIR / MEMORY_FILE


def _safe_file(root: Path, file_path: str | Path) -> Path:
    candidate = (root / file_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"file path escapes working directory: {file_path}") from exc
    if not candidate.is_file():
        raise ValueError(f"file path does not exist: {file_path}")
    return candidate


def _read_excerpt(path: Path, max_bytes: int) -> tuple[str, bool]:
    raw = path.read_bytes()
    truncated = len(raw) > max_bytes
    sample = raw[:max_bytes]
    text = sample.decode("utf-8", errors="replace")
    return text, truncated


def build_context_packet(
    *,
    task_description: str,
    working_dir: str | Path = ".",
    file_paths: list[str] | None = None,
    source_urls: list[str] | None = None,
    max_files: int = 12,
    max_bytes_per_file: int = 4000,
) -> ContextPacket:
    """Build a compact context packet from repo files and source URLs."""
    root = Path(working_dir).resolve()
    sources = [source for source in (source_urls or []) if source.strip()]
    recon = phase0_recon(
        task_description=task_description,
        working_dir=root,
        provided_sources=sources,
        max_relevant_files=max_files,
    )

    selected_paths = list(file_paths or recon.codebase.relevant_files)[:max_files]
    warnings: list[str] = list(recon.required_actions)
    files: list[ContextFile] = []

    for rel in selected_paths:
        try:
            path = _safe_file(root, rel)
            excerpt, truncated = _read_excerpt(path, max_bytes_per_file)
        except (OSError, ValueError) as exc:
            warnings.append(str(exc))
            continue

        raw = path.read_bytes()
        files.append(ContextFile(
            path=path.relative_to(root).as_posix(),
            sha256=hashlib.sha256(raw).hexdigest(),
            size_bytes=len(raw),
            excerpt=excerpt,
            truncated=truncated,
        ))

    return ContextPacket(
        task_description=task_description,
        recon_verdict=recon.verdict,
        source_urls=sources,
        files=files,
        warnings=warnings,
    )


def store_vector_memory(
    *,
    text: str,
    namespace: str = "default",
    metadata: dict[str, Any] | None = None,
    working_dir: str | Path = ".",
) -> VectorMemoryStoreResult:
    """Store a text memory as a local vector record."""
    if not text.strip():
        raise ValueError("text must not be empty")
    namespace = namespace.strip() or "default"
    path = _memory_path(working_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(UTC).isoformat()
    digest = hashlib.sha256(f"{namespace}\0{text}\0{created_at}".encode()).hexdigest()
    record = VectorMemoryRecord(
        id=digest[:24],
        namespace=namespace,
        text=text,
        vector=vector_embed(text),
        metadata=metadata or {},
        created_at=created_at,
    )
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record.model_dump(), separators=(",", ":")) + "\n")

    return VectorMemoryStoreResult(
        id=record.id,
        namespace=namespace,
        path=str(path),
    )


def _iter_memory(path: Path) -> list[VectorMemoryRecord]:
    if not path.exists():
        return []

    records: list[VectorMemoryRecord] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            records.append(VectorMemoryRecord.model_validate_json(line))
        except ValueError:
            continue
    return records


def _dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=False))


def _resolve_min_score(min_score: float | None) -> float:
    """Effective similarity floor: explicit arg wins, else env, else 0.0."""
    if min_score is not None:
        return max(-1.0, min(1.0, float(min_score)))
    raw = os.environ.get(_ENV_MIN_SCORE, "").strip()
    if not raw:
        return 0.0
    try:
        return max(-1.0, min(1.0, float(raw)))
    except ValueError:
        return 0.0


def query_vector_memory(
    *,
    query: str,
    namespace: str = "default",
    top_k: int = 5,
    working_dir: str | Path = ".",
    min_score: float | None = None,
) -> VectorMemoryQueryResult:
    """Return nearest local vector memories for a query.

    Scores are cosine similarities for L2-normalized hashing embeddings (dot product).
    Results with score strictly below ``min_score`` (after resolution) are omitted
    from ``matches`` but counted in ``below_threshold_omitted``.
    """
    if not query.strip():
        raise ValueError("query must not be empty")
    namespace = namespace.strip() or "default"
    top_k = max(1, min(int(top_k), 25))
    floor = _resolve_min_score(min_score)

    query_vector = vector_embed(query)
    scored: list[tuple[float, VectorMemoryRecord]] = []
    for record in _iter_memory(_memory_path(working_dir)):
        if record.namespace != namespace:
            continue
        scored.append((_dot(query_vector, record.vector), record))

    scored.sort(key=lambda item: item[0], reverse=True)
    omitted = sum(1 for score, _ in scored if score < floor)
    eligible = [(score, record) for score, record in scored if score >= floor]
    matches = [
        VectorMemoryMatch(
            id=record.id,
            namespace=record.namespace,
            score=round(score, 6),
            text=record.text,
            metadata=record.metadata,
            created_at=record.created_at,
        )
        for score, record in eligible[:top_k]
    ]
    return VectorMemoryQueryResult(
        query=query,
        namespace=namespace,
        matches=matches,
        min_score_applied=floor,
        below_threshold_omitted=omitted,
    )
