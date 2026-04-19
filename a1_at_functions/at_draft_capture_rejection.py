# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_loraflywheel.py:115
# Component id: at.source.ass_ade.capture_rejection
__version__ = "0.1.0"

    def capture_rejection(self, candidate: str, reason: str, confidence: float = 0.9) -> str:
        """Capture a CIE-rejected candidate as a negative training example."""
        if not self._enabled:
            return ""
        cid = f"rejection_{int(time.time())}_{len(self._pending)}"
        c = Contribution(
            kind="rejection",
            content={"candidate": candidate[:2000], "reason": reason[:200]},
            session_id=self._session_id,
            confidence=confidence,
        )
        self._pending.append(c)
        self._save_pending()
        return cid
