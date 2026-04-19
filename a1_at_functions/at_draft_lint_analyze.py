# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_lint_analyze.py:7
# Component id: at.source.a1_at_functions.lint_analyze
from __future__ import annotations

__version__ = "0.1.0"

def lint_analyze(
    self,
    path_analysis: dict[str, Any],
    agent_id: str | None = None,
) -> LintResult:
    """Run monadic lint analysis via AAAA-Nexus synthesis engine."""
    payload: dict[str, Any] = {"path_analysis": path_analysis}
    if agent_id:
        payload["agent_id"] = agent_id
    return self._post_model("/v1/lint/analyze", LintResult, payload)
