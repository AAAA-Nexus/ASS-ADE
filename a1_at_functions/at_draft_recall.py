# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_edee.py:44
# Component id: at.source.ass_ade.recall
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
