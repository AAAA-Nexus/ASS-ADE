# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_capture_rejection.py:7
# Component id: at.source.a1_at_functions.capture_rejection
from __future__ import annotations

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
