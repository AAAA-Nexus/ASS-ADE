# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:788
# Component id: mo.source.ass_ade.spending_budget
__version__ = "0.1.0"

    def spending_budget(
        self,
        chain: list[dict] | None = None,
        total_usdc: float = 0.0,
        *,
        agent_id: str | None = None,
        **kwargs: Any,
    ) -> SpendingBudgetResult:
        """/v1/spending/budget — multi-hop chain budget (SPG-101). $0.040/call"""
        resolved_chain = chain or ([{"agent_id": agent_id}] if agent_id else [])
        return self._post_model("/v1/spending/budget", SpendingBudgetResult, {"chain": resolved_chain, "total_usdc": total_usdc, **kwargs})
