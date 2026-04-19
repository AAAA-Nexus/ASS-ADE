# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:899
# Component id: mo.source.ass_ade.saga_compensate
__version__ = "0.1.0"

    def saga_compensate(self, saga_id: str, **kwargs: Any) -> CompensationResult:
        """/v1/rollback/saga/{id}/compensate — LIFO rollback (RBK-100). $0.040/call"""
        return self._post_model(f"/v1/rollback/saga/{_pseg(saga_id, 'saga_id')}/compensate", CompensationResult, kwargs or {})
