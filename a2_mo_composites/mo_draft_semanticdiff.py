# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_semanticdiff.py:7
# Component id: mo.source.a2_mo_composites.semanticdiff
from __future__ import annotations

__version__ = "0.1.0"

class SemanticDiff(NexusModel):
    """/v1/agents/semantic-diff"""
    drift_score: float | None = None
    jaccard_similarity: float | None = None
    changed_concepts: list[str] = Field(default_factory=list)
