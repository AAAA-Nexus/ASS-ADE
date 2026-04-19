# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/alphaverus.py:179
# Component id: at.source.ass_ade.verify
__version__ = "0.1.0"

    def verify(self, code: str, spec: str) -> bool:
        if self._nexus is not None and hasattr(self._nexus, "certify_output_verify"):
            try:
                result = self._nexus.certify_output_verify(code)
                verdict = getattr(result, "rubric_passed", None)
                if verdict is not None:
                    return bool(verdict)
            except Exception:
                pass
        metrics = _score(code, spec)
        return _passes(metrics)
