

"""
Vector DB Backend Abstraction for ASS-ADE.
Supports pluggable adapters (Chroma, Qdrant, etc.).
Hardened with type hints, error handling, and logging.
"""

from typing import Any, List, Dict, Optional
import logging

logger = logging.getLogger("ass_ade.vector_db_backend")


class VectorDBBackend:
    """
    Abstraction for pluggable vector DB backends.
    """
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.adapter: Optional[Any] = None
        self.configure(self.config)

    def configure(self, config: dict):
        backend = config.get("backend", "chroma")
        if backend == "chroma":
            self.adapter = ChromaAdapter(config)
        else:
            raise ValueError(f"Unknown vector DB backend: {backend}")

    def add(self, text: str, metadata: dict) -> str:
        if not self.adapter:
            raise RuntimeError("No vector DB adapter configured.")
        return self.adapter.add(text, metadata)

    def query(self, text: str, top_k: int = 5) -> List[dict]:
        if not self.adapter:
            raise RuntimeError("No vector DB adapter configured.")
        return self.adapter.query(text, top_k)

    def delete(self, id: str) -> None:
        if not self.adapter:
            raise RuntimeError("No vector DB adapter configured.")
        self.adapter.delete(id)


class ChromaAdapter:
    """
    Minimal in-memory Chroma-like adapter for demo/testing.
    """
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self._store: List[Dict[str, Any]] = []  # {id, text, metadata, embedding}
        self._id_counter = 0

    def add(self, text: str, metadata: dict) -> str:
        _id = f"vec_{self._id_counter}"
        self._id_counter += 1
        self._store.append({"id": _id, "text": text, "metadata": metadata, "embedding": self._fake_embed(text)})
        return _id

    def query(self, text: str, top_k: int = 5) -> List[dict]:
        emb = self._fake_embed(text)
        scored = [
            {**rec, "score": self._dot(rec["embedding"], emb)}
            for rec in self._store
        ]
        return sorted(scored, key=lambda r: r["score"], reverse=True)[:top_k]

    def delete(self, id: str) -> None:
        before = len(self._store)
        self._store = [rec for rec in self._store if rec["id"] != id]
        after = len(self._store)
        if before == after:
            logger.warning(f"No vector found with id: {id}")

    def _fake_embed(self, text: str) -> List[float]:
        # Simple hash-based fake embedding (not for production)
        return [float(ord(c)) % 13 for c in text[:16].ljust(16)]

    def _dot(self, a: List[float], b: List[float]) -> float:
        return sum(x*y for x, y in zip(a, b))
