# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_loraflywheel.py:253
# Component id: at.source.ass_ade.status
__version__ = "0.1.0"

    def status(self) -> LoRAStatus:
        kind_counts: dict[str, int] = {}
        for c in self._pending:
            kind_counts[c.kind] = kind_counts.get(c.kind, 0) + 1

        adapter_version = self._adapter_version
        quality_score = 0.0
        if self._nexus:
            try:
                s = getattr(self._nexus, "lora_adapter_current", lambda: None)()
                if s:
                    adapter_version = str(getattr(s, "version", adapter_version))
                    quality_score = float(getattr(s, "quality_score", 0.0))
            except Exception:
                pass

        next_batch = self._batch_interval - (self._step_count % self._batch_interval)
        return LoRAStatus(
            adapter_version=adapter_version,
            contribution_count=self._total_contributed + len(self._pending),
            principle_count=kind_counts.get("principle", 0),
            fix_count=kind_counts.get("fix", 0),
            rejection_count=kind_counts.get("rejection", 0),
            ratchet_epoch=self._ratchet_epoch,
            pending_count=len(self._pending),
            next_batch_step=next_batch,
            quality_score=quality_score,
        )
