# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:371
# Component id: mo.source.ass_ade.semanticdiff
from __future__ import annotations

__version__ = "0.1.0"

class SemanticDiff(NexusModel):
    """/v1/agents/semantic-diff"""
    drift_score: float | None = None
    jaccard_similarity: float | None = None
    changed_concepts: list[str] = Field(default_factory=list)
