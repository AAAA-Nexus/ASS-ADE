# Extracted from C:/!ass-ade/src/ass_ade/agent/edee.py:63
# Component id: at.source.ass_ade.recall
from __future__ import annotations

__version__ = "0.1.0"

def recall(self, task_embedding: Any, k: int = 5) -> list[dict]:
    q = task_embedding if isinstance(task_embedding, str) else str(task_embedding)
    result = query_vector_memory(
        query=q,
        namespace=EXPERIENCE_NS,
        top_k=k,
        working_dir=self._working_dir,
    )
    return [{"id": m.id, "score": m.score, "text": m.text, "metadata": m.metadata} for m in result.matches]
