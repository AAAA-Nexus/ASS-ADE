# Extracted from C:/!ass-ade/src/ass_ade/agent/lora_flywheel.py:159
# Component id: at.source.ass_ade.capture_principle
from __future__ import annotations

__version__ = "0.1.0"

def capture_principle(self, principle: str, confidence: float = 0.8) -> str:
    """Capture a WisdomEngine-distilled principle as a training signal."""
    if not self._enabled or confidence < self._min_confidence:
        return ""
    cid = f"principle_{int(time.time())}_{len(self._pending)}"
    c = Contribution(
        kind="principle",
        content={"principle": principle[:500]},
        session_id=self._session_id,
        confidence=confidence,
    )
    self._pending.append(c)
    self._save_pending()
    return cid
