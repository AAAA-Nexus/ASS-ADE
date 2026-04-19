# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_recall.py:7
# Component id: at.source.a1_at_functions.recall
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
