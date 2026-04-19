# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_lifrgraph.py:16
# Component id: mo.source.ass_ade.store
__version__ = "0.1.0"

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
