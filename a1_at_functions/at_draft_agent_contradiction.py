# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_agent_contradiction.py:7
# Component id: at.source.a1_at_functions.agent_contradiction
from __future__ import annotations

__version__ = "0.1.0"

def agent_contradiction(self, statement_a: str, statement_b: str, **kwargs: Any) -> ContradictionResult:
    """/v1/agents/contradiction — NLI fact-checker for two statements. $0.020/request"""
    return self._post_model("/v1/agents/contradiction", ContradictionResult, {
        "statement_a": statement_a, "statement_b": statement_b, **kwargs,
    })
