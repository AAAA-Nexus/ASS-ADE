# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/resilience.py:154
# Component id: at.source.ass_ade.is_open
__version__ = "0.1.0"

    def is_open(self) -> bool:
        if self._open_since is None:
            return False
        if time.monotonic() - self._open_since >= self._recovery_s:
            return False  # half-open: allow a probe
        return True
