# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:446
# Component id: mo.source.ass_ade.entropy_oracle
__version__ = "0.1.0"

    def entropy_oracle(self, **kwargs: Any) -> EntropyResult:
        """/v1/oracle/entropy — session entropy measurement. $0.004/call"""
        return self._post_model("/v1/oracle/entropy", EntropyResult, kwargs or {})
