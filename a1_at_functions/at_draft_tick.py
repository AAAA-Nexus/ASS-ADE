# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_loraflywheel.py:132
# Component id: at.source.ass_ade.tick
__version__ = "0.1.0"

    def tick(self) -> BatchResult | None:
        """Advance step counter. Returns BatchResult if batch was submitted."""
        self._step_count += 1
        if self._step_count % self._batch_interval == 0 and self._pending:
            return self.contribute_batch()
        return None
