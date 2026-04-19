# Extracted from C:/!ass-ade/src/ass_ade/agent/lora_flywheel.py:143
# Component id: at.source.ass_ade.capture_fix
from __future__ import annotations

__version__ = "0.1.0"

def capture_fix(self, original: str, fixed: str, context: dict[str, Any] | None = None) -> str:
    """Capture a before/after code fix as a positive training signal."""
    if not self._enabled:
        return ""
    cid = f"fix_{int(time.time())}_{len(self._pending)}"
    c = Contribution(
        kind="fix",
        content={"original": original[:2000], "fixed": fixed[:2000], "context": context or {}},
        session_id=self._session_id,
        confidence=1.0,
    )
    self._pending.append(c)
    self._save_pending()
    self._maybe_batch()
    return cid
