# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:998
# Component id: mo.source.ass_ade.defi_risk_score
__version__ = "0.1.0"

    def defi_risk_score(self, protocol: str, position: dict | None = None, **kwargs: Any) -> DefiRiskScore:
        """/v1/defi/risk-score — risk + max drawdown bound 12.5% (DFI-101). $0.08/call"""
        return self._post_model("/v1/defi/risk-score", DefiRiskScore, {"protocol": protocol, "position": position or {}, **kwargs})
