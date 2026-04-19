# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_edee.py:20
# Component id: at.source.ass_ade.capture_trace
__version__ = "0.1.0"

    def capture_trace(self, phase: str, data: dict) -> str:
        text = f"[{phase}] {data.get('summary', str(data)[:200])}"
        meta = {"phase": phase, "data": data, "kind": "trace"}
        result = store_vector_memory(
            text=text,
            namespace=EXPERIENCE_NS,
            metadata=meta,
            working_dir=self._working_dir,
        )
        self._traces += 1
        return result.id
