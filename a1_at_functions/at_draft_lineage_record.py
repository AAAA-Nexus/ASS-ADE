# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lineage_record.py:7
# Component id: at.source.a1_at_functions.lineage_record
from __future__ import annotations

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
