# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:800
# Component id: mo.source.ass_ade.lineage_record
__version__ = "0.1.0"

    def lineage_record(
        self,
        intent: str | None = None,
        constraints: list[str] | None = None,
        outcome: str | None = None,
        *,
        agent_id: str | None = None,
        action: str | None = None,
        **kwargs: Any,
    ) -> LineageRecord:
        """/v1/lineage/record — hash-chained audit record (DLV-100). $0.060/call"""
        resolved_intent = intent or action or (f"agent:{agent_id}" if agent_id else "record")
        resolved_constraints = constraints or ([f"agent_id:{agent_id}"] if agent_id else [])
        resolved_outcome = outcome or action or "recorded"
        return self._post_model("/v1/lineage/record", LineageRecord, {
            "intent": resolved_intent, "constraints": resolved_constraints, "outcome": resolved_outcome, **kwargs,
        })
