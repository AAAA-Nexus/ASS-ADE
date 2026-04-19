# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:895
# Component id: mo.source.ass_ade.saga_checkpoint
__version__ = "0.1.0"

    def saga_checkpoint(self, saga_id: str, step: str, **kwargs: Any) -> SagaCheckpoint:
        """/v1/rollback/saga/{id}/checkpoint — mark step completed (RBK-100). $0.020/call"""
        return self._post_model(f"/v1/rollback/saga/{_pseg(saga_id, 'saga_id')}/checkpoint", SagaCheckpoint, {"step": step, **kwargs})
