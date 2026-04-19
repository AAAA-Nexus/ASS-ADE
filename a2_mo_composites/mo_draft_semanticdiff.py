# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:371
# Component id: mo.source.ass_ade.semanticdiff
__version__ = "0.1.0"

class SemanticDiff(NexusModel):
    """/v1/agents/semantic-diff"""
    drift_score: float | None = None
    jaccard_similarity: float | None = None
    changed_concepts: list[str] = Field(default_factory=list)
