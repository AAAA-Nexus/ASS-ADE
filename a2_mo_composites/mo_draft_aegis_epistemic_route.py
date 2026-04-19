# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:756
# Component id: mo.source.ass_ade.aegis_epistemic_route
__version__ = "0.1.0"

    def aegis_epistemic_route(
        self,
        prompt: str | None = None,
        max_tokens: int = 256,
        model: str = "auto",
        *,
        query: str | None = None,
        **kwargs: Any,
    ) -> EpistemicRouteResult:
        """/v1/aegis/router/epistemic-bound — epistemic-aware routing (AEG-101). $0.040/call"""
        return self._post_model("/v1/aegis/router/epistemic-bound", EpistemicRouteResult, {
            "prompt": prompt or query or "", "max_tokens": max_tokens, "model": model, **kwargs,
        })
